"""
Grille de fond infinie avec déformation type lentille gravitationnelle.

La grille est définie dans l'espace monde, recadrée par la caméra, avec un pas
qui s'adapte au zoom (subdivision progressive). Chaque point est déplacé selon
un champ inspiré du potentiel newtonien (effet visuel, pas une ray-tracing GR).
"""

from __future__ import annotations

import math
from typing import Any, List, Tuple

import pygame


def _interpolated_xy(obj: Any, alpha: float) -> Tuple[float, float]:
    px = float(obj.prev_x) + (float(obj.x) - float(obj.prev_x)) * alpha
    py = float(obj.prev_y) + (float(obj.y) - float(obj.prev_y)) * alpha
    return px, py


def _gather_lens_sources(
    engine: Any,
    alpha: float,
    circles: List[Any],
    visible_diagonal: float,
) -> List[Tuple[float, float, float, float]]:
    """
    Retourne une liste de (wx, wy, masse, adoucissement_m) pour chaque source.

    Seuls les corps présents dans ``circles`` (déjà créés / simulés) sont pris
    en compte — pas le ``temp_circle`` en cours de création à la souris.

    L'adoucissement évite la singularité au centre tout en restant **petit**
    devant l'étendue visible du jeu. Une valeur engine ``grid_lens_softening_world``
    > 0 force un plancher absolu ; sinon on utilise une fraction de la diagonale
    visible + le rayon du corps.
    """
    sources: List[Tuple[float, float, float, float]] = []

    diag = max(visible_diagonal, 1.0)
    cfg_soft = float(getattr(engine, "grid_lens_softening_world", 0.0))
    floor_from_view = diag * 0.002

    for c in circles:
        if getattr(c, "suicide", False):
            continue
        wx, wy = _interpolated_xy(c, alpha)
        m = float(c.mass)
        if m <= 0:
            continue
        rad = float(getattr(c, "radius", 0.0))
        if cfg_soft > 0:
            soft = max(cfg_soft, rad * 0.5, 1.0)
        else:
            soft = max(rad * 0.75, floor_from_view, 8.0)
        sources.append((wx, wy, m, soft))

    return sources


def _deflect(
    wx: float,
    wy: float,
    sources: List[Tuple[float, float, float, float]],
    engine: Any,
    visible_diagonal: float,
    cam_scale: float,
) -> Tuple[float, float]:
    """
    Déplace (wx, wy) vers les masses (effet type lentille faible).

    Principe : on veut un déplacement **visible en pixels** après projection,
    quelle que soit la constante ``camera.scale`` (zoom). La caméra fait
    ``screen_delta = world_delta * scale`` ; on impose donc un déplacement
    monde ``world_delta ≈ (cible en px) / scale``.

    Pour chaque masse : contribution radiale ``(dx, dy)/r`` fois une amplitude
    ``A * (m/M_ref) * falloff(r)`` où ``falloff = soft² / (r² + soft²)`` vaut
    ~1 près du centre et décroît loin (évite singularité). ``M_ref`` est la
    masse max parmi les sources pour normaliser les corps légers / lourds.

    ``visible_diagonal`` borne l'amplitude max (avec ``cap_world``) pour éviter
    des sauts énormes si beaucoup de masses se superposent.
    """
    if not sources:
        return wx, wy

    amount = max(0.0, float(getattr(engine, "grid_lens_amount", 1.0)))
    if amount <= 0.0:
        return wx, wy

    cam_scale = max(float(cam_scale), 1e-15)
    mass_ref = max(float(getattr(engine, "grid_lens_mass_ref", 1e6)), 1.0)
    target_px = float(getattr(engine, "grid_target_spacing_px", 72.0))
    inv_sign = -1.0 if getattr(engine, "reversed_gravity", False) else 1.0

    # sqrt(scale) : zoom in → plus visible, zoom out → moins visible
    # Garantit l'absence de croisement si soft ≥ amount/(2*sqrt(scale))
    # Avec soft ≥ 12 et amount ≤ ~24, condition toujours satisfaite.
    zoom_factor = math.sqrt(cam_scale)
    cap_world = 0.38 * target_px / cam_scale  # sécurité pour amount élevé

    gx = 0.0
    gy = 0.0
    for cx, cy, mass, soft in sources:
        dx = cx - wx
        dy = cy - wy
        r2_eps = dx * dx + dy * dy + soft * soft
        r = math.sqrt(r2_eps)
        if r < 1e-15:
            continue

        falloff = (soft * soft) / r2_eps
        w = mass / mass_ref

        disp_px = amount * zoom_factor * w * falloff
        mag_world = min(disp_px / cam_scale, cap_world)

        gx += inv_sign * mag_world * dx / r
        gy += inv_sign * mag_world * dy / r

    return wx + gx, wy + gy


def _nice_world_cell(rough: float) -> float:
    """Arrondit le pas monde à 1, 2 ou 5 × 10^k pour une grille lisible."""
    if rough <= 0 or not math.isfinite(rough):
        return 1.0
    exp10 = math.floor(math.log10(rough))
    base = 10.0**exp10
    mant = rough / base
    if mant <= 1.0:
        return base
    if mant <= 2.0:
        return 2.0 * base
    if mant <= 5.0:
        return 5.0 * base
    return 10.0 * base


def draw_gravitational_grid(
    screen: pygame.Surface,
    engine: Any,
    alpha: float,
    circles: List[Any],
) -> None:
    """Dessine la grille derrière les corps (appeler après le fond, avant les astres)."""
    if not getattr(engine, "gravitational_grid_enabled", False):
        return

    sw = screen.get_width()
    sh = screen.get_height()
    cam = engine.camera

    # Coins écran → monde (rectangle visible)
    corners = [
        cam.screen_to_world(0, 0),
        cam.screen_to_world(sw, 0),
        cam.screen_to_world(sw, sh),
        cam.screen_to_world(0, sh),
    ]
    wxs = [c[0] for c in corners]
    wys = [c[1] for c in corners]
    w_min, w_max = min(wxs), max(wxs)
    h_min, h_max = min(wys), max(wys)

    # Marge pour que les lignes courbes restent visibles près des bords
    span = max(w_max - w_min, h_max - h_min, 1.0)
    margin = span * 0.35
    w_min -= margin
    w_max += margin
    h_min -= margin
    h_max += margin

    visible_diagonal = math.hypot(w_max - w_min, h_max - h_min)

    target_px = float(getattr(engine, "grid_target_spacing_px", 72.0))
    scale = float(cam.scale)
    if scale <= 0 or not math.isfinite(scale):
        return

    rough_cell = target_px / scale
    cell_major = _nice_world_cell(rough_cell)

    max_lines = int(getattr(engine, "grid_max_lines", 96))
    n_vert = int((w_max - w_min) / cell_major) + 2
    n_horz = int((h_max - h_min) / cell_major) + 2
    if n_vert > max_lines or n_horz > max_lines:
        factor = max(n_vert / max_lines, n_horz / max_lines, 1.0)
        cell_major *= factor
        cell_major = _nice_world_cell(cell_major)

    i0 = int(math.floor(w_min / cell_major))
    i1 = int(math.ceil(w_max / cell_major))
    j0 = int(math.floor(h_min / cell_major))
    j1 = int(math.ceil(h_max / cell_major))

    # Limite stricte sur le nombre de lignes pour les perfs
    if (i1 - i0) > max_lines:
        mid = (i0 + i1) // 2
        half = max_lines // 2
        i0, i1 = mid - half, mid + half
    if (j1 - j0) > max_lines:
        mid = (j0 + j1) // 2
        half = max_lines // 2
        j0, j1 = mid - half, mid + half

    sources = _gather_lens_sources(engine, alpha, circles, visible_diagonal)

    dark = getattr(engine, "screen_mode", "dark") == "dark"
    if dark:
        col_major = (48, 54, 68)
        col_minor = (38, 42, 54)
    else:
        col_major = (190, 192, 210)
        col_minor = (210, 212, 225)

    major_px = cell_major * scale
    subdivide = major_px > float(getattr(engine, "grid_subdivide_px", 96.0))
    cell_minor = cell_major / 5.0 if subdivide else None

    # Pas d'échantillonnage le long d'une ligne (monde) : ~8 px à l'écran
    sample_world = max(8.0 / scale, cell_major * 0.08, 1.0)

    def world_to_screen(wx: float, wy: float) -> Tuple[int, int]:
        px, py = _deflect(wx, wy, sources, engine, visible_diagonal, scale)
        sx, sy = cam.world_to_screen(px, py)
        return int(round(sx)), int(round(sy))

    def draw_polyline_world(
        get_xy,
        t_min: float,
        t_max: float,
        color: Tuple[int, int, int],
        width: int = 1,
    ) -> None:
        if t_max < t_min:
            t_min, t_max = t_max, t_min
        n = max(2, int(math.ceil((t_max - t_min) / sample_world)) + 1)
        step = (t_max - t_min) / (n - 1) if n > 1 else 0.0
        pts: List[Tuple[int, int]] = []
        for k in range(n):
            t = t_min + k * step
            wx, wy = get_xy(t)
            pts.append(world_to_screen(wx, wy))
        if len(pts) >= 2:
            pygame.draw.lines(screen, color, False, pts, width)

    # --- Grille mineure (1/5 du pas principal si zoom suffisant) ---
    if cell_minor is not None and cell_minor > 0:
        mi0 = int(math.floor(w_min / cell_minor))
        mi1 = int(math.ceil(w_max / cell_minor))
        mj0 = int(math.floor(h_min / cell_minor))
        mj1 = int(math.ceil(h_max / cell_minor))
        dense_ok = (mi1 - mi0) <= 80 and (mj1 - mj0) <= 80
        if dense_ok and (mi1 - mi0) <= max_lines * 5 and (mj1 - mj0) <= max_lines * 5:
            for ii in range(mi0, mi1 + 1):
                xw = ii * cell_minor
                if abs(xw / cell_major - round(xw / cell_major)) < 1e-6:
                    continue
                draw_polyline_world(lambda t, x=xw: (x, t), h_min, h_max, col_minor, 1)
            for jj in range(mj0, mj1 + 1):
                yw = jj * cell_minor
                if abs(yw / cell_major - round(yw / cell_major)) < 1e-6:
                    continue
                draw_polyline_world(lambda t, y=yw: (t, y), w_min, w_max, col_minor, 1)

    # --- Grille majeure ---
    for ii in range(i0, i1 + 1):
        xw = ii * cell_major
        draw_polyline_world(lambda t, x=xw: (x, t), h_min, h_max, col_major, 1)
    for jj in range(j0, j1 + 1):
        yw = jj * cell_major
        draw_polyline_world(lambda t, y=yw: (t, y), w_min, w_max, col_major, 1)
