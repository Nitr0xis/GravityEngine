# GravityEngine — N-body gravitational simulator
# Copyright (C) 2026 Nils DONTOT
# Contact: nils.dontot.pro@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Infinite background grid with gravitational lensing-like deformation.

The grid is defined in world space, clipped by the camera, with a step
that adapts to zoom (progressive subdivision). Each point is moved according
to a field inspired by the Newtonian potential (visual effect, not GR ray-tracing).
"""

from __future__ import annotations

import math
import numpy as np
from typing import Any, List, Tuple

import pygame


def _interpolated_xy(obj: Any, alpha: float) -> Tuple[float, float]:
    px = float(obj.prev_x) + (float(obj.x) - float(obj.prev_x)) * alpha
    py = float(obj.prev_y) + (float(obj.y) - float(obj.prev_y)) * alpha
    return px, py


def _gather_lens_sources(engine, alpha, circles):
    sources = []

    cfg_soft = float(getattr(engine, "grid_lens_softening_world", 0.0))

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
            # Only the physical radius of the object, plus a tiny absolute floor to avoid the singularity at r=0.
            soft = max(rad * 0.75, 1.0)
        sources.append((wx, wy, m, soft))

    return sources


def _deflect_batch(points, sources, amount, cam_scale, mass_ref, target_px, inv_sign):
    if amount <= 0.0 or sources.shape[0] == 0:
        return points

    cam_scale = max(cam_scale, 1e-15)
    zoom_factor = math.sqrt(cam_scale)
    cap_world = 0.38 * target_px / cam_scale

    px = points[:, 0][:, None]
    py = points[:, 1][:, None]
    sx = sources[:, 0][None, :]
    sy = sources[:, 1][None, :]
    mass = sources[:, 2][None, :]
    soft = sources[:, 3][None, :]

    dx = sx - px
    dy = sy - py
    r = np.sqrt(dx * dx + dy * dy)
    r_safe = np.maximum(r, 1e-15)

    # Decay as 1/(r+soft): correct form (~ 1/b like Einstein's formula), softening is only to avoid the singularity at r=0.
    falloff = soft / (r + soft)
    w = mass / mass_ref

    disp_px = amount * zoom_factor * w * falloff
    mag_world = np.minimum(disp_px / cam_scale, cap_world)

    gx = inv_sign * np.sum(mag_world * dx / r_safe, axis=1)
    gy = inv_sign * np.sum(mag_world * dy / r_safe, axis=1)

    return points + np.stack([gx, gy], axis=1)


def _nice_world_cell(rough: float) -> float:
    """Rounds the world grid step to 1, 2, or 5 × 10^k for a clean, readable grid."""
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
    """Draws the grid behind the bodies (call after the background, before celestial bodies)."""
    if not getattr(engine, "gravitational_grid_enabled", False):
        return

    sw = screen.get_width()
    sh = screen.get_height()
    cam = engine.camera

    # Screen corners → world (visible rectangle)
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

    # Margin so that curved lines remain visible near the edges
    span = max(w_max - w_min, h_max - h_min, 1.0)
    margin = span * 0.35
    w_min -= margin
    w_max += margin
    h_min -= margin
    h_max += margin

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

    # Strict limit on number of lines for performance
    if (i1 - i0) > max_lines:
        mid = (i0 + i1) // 2
        half = max_lines // 2
        i0, i1 = mid - half, mid + half
    if (j1 - j0) > max_lines:
        mid = (j0 + j1) // 2
        half = max_lines // 2
        j0, j1 = mid - half, mid + half

    sources = _gather_lens_sources(engine, alpha, circles)

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

    # Sampling interval along a line (in world units): ~8 px on the screen
    sample_world = max(8.0 / scale, cell_major * 0.08, 1.0)

    mass_ref = max(float(getattr(engine, "grid_lens_mass_ref", 1e6)), 1.0)
    amount = max(0.0, float(getattr(engine, "grid_lens_amount", 1.0)))
    inv_sign = -1.0 if getattr(engine, "reversed_gravity", False) else 1.0

    sources_arr = (np.array(sources, dtype=np.float64)
                   if sources else np.zeros((0, 4)))

    # --- Build line specs (major + minor), without drawing yet ---
    line_specs: List[Tuple[Any, float, float, Tuple[int, int, int], int]] = []

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
                line_specs.append((lambda t, x=xw: (x, t), h_min, h_max, col_minor, 1))
            for jj in range(mj0, mj1 + 1):
                yw = jj * cell_minor
                if abs(yw / cell_major - round(yw / cell_major)) < 1e-6:
                    continue
                line_specs.append((lambda t, y=yw: (t, y), w_min, w_max, col_minor, 1))

    for ii in range(i0, i1 + 1):
        xw = ii * cell_major
        line_specs.append((lambda t, x=xw: (x, t), h_min, h_max, col_major, 1))
    for jj in range(j0, j1 + 1):
        yw = jj * cell_major
        line_specs.append((lambda t, y=yw: (t, y), w_min, w_max, col_major, 1))

    # --- Sample all points, only once ---
    all_points: List[Tuple[float, float]] = []
    line_slices: List[Tuple[int, int, Tuple[int, int, int], int]] = []

    for get_xy, t_min, t_max, color, width in line_specs:
        if t_max < t_min:
            t_min, t_max = t_max, t_min
        n = max(2, int(math.ceil((t_max - t_min) / sample_world)) + 1)
        step = (t_max - t_min) / (n - 1) if n > 1 else 0.0
        start = len(all_points)
        for k in range(n):
            all_points.append(get_xy(t_min + k * step))
        line_slices.append((start, len(all_points), color, width))

    if not all_points:
        return

    points_arr = np.array(all_points, dtype=np.float64)
    deflected = _deflect_batch(points_arr, sources_arr, amount, scale,
                                mass_ref, target_px, inv_sign)

    # --- Drawing: reproject to screen + draw line by line ---
    cam_x, cam_y = cam.cam_x, cam.cam_y
    for start, end, color, width in line_slices:
        seg = deflected[start:end]
        screen_pts = [
            (int(round(x * scale + cam_x)), int(round(y * scale + cam_y)))
            for x, y in seg
        ]
        if len(screen_pts) >= 2:
            pygame.draw.lines(screen, color, False, screen_pts, width)
    