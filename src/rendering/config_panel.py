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
Pygame Configuration Panel for Gravity Engine
==============================================

Overlay-style configuration panel with custom widgets.
Press C to open, ESC or click outside to close.

Author: Nils DONTOT
Version: 1.0.0
"""

import pygame
import json

from core.logger import Logger
from core import state
from rendering.ui_widgets import C, Widget, SectionTitle, Checkbox, Toggle, Slider, Button


# ==================================================================================
# MAIN PANEL
# ==================================================================================

class ConfigPanel:
    def __init__(self, engine, screen, font_path):
        self.engine, self.screen = engine, screen
        self.font_big = pygame.font.Font(font_path, int(28 * state.engine.scale_coefficient))
        self.font_med = pygame.font.Font(font_path, int(20 * state.engine.scale_coefficient))
        self.font_sm = pygame.font.Font(font_path, int(16 * state.engine.scale_coefficient))
        
        self.visible = False
        self.widgets = []
        
        # Panel rect
        self.pw, self.ph = int(650 * state.engine.scale_coefficient), int(750 * state.engine.scale_coefficient)
        self.px = (screen.get_width() - self.pw) // 2
        self.py = (screen.get_height() - self.ph) // 2
        self.panel_rect = pygame.Rect(self.px, self.py, self.pw, self.ph)
        
        # Scroll
        self.scroll = 0
        self.max_scroll = 0
        
        self._build()
    
    def _build(self):
        self.widgets.clear()
        # Espace laissé en haut pour le titre et la barre — à synchroniser avec le draw() ci-dessous
        y_offset_top = int(70 * state.engine.scale_coefficient)
        x, y = self.px + 25, self.py + y_offset_top
        w = (self.pw - 50)
        
        # === SIMULATION ===
        y = self._sec(x, y, "Simulation")
        y = self._slider(x, y, w, "Target FPS", "FPS_TARGET",
                         30, 240, False, "{:.0f} FPS")
        y = self._slider(x, y, w, "Time Acceleration", "time_acceleration",
                         1e0, 5e5, True, "{:.2e}x")
        
        # === PHYSICS ===
        y = self._sec(x, y, "Physics")
        y = self._checkbox(x, y, "Enable Reversed Gravity", "reversed_gravity")
        y = self._checkbox(x, y, "Enable Random Speed Mode", "random_mode")
        y = self._slider(x, y, w, "Corpses Density", "default_density",
                         1e0, 1e5, True, "{:.2e} kg/m³")
        y = self._checkbox(x, y, "Enable Body Fusions", "fusions")
        y = self._slider(x, y, w, "Barnes-Hut Theta", "barnes_hut_theta",
                 0.0, 1.5, False, "{:.2f}")
        y = self._slider(x, y, w, "Random Environment Generation Bodies Number", "random_environment_number",
                 1, 200, False, "{:.0f} bodies")
        
        # === VISUAL ===
        y = self._sec(x, y, "Visual")
        y = self._slider(x, y, w, "Camera Zoom", "camera_zoom",
                         self.engine.camera.min_scale, self.engine.camera.max_scale, True, "{:.2e}x")
        y = self._checkbox(x, y, "Show Vectors", "vectors_printed")
        y = self._slider(x, y, w, "Vector Scale", "vector_scale",
                         0.1, 10.0, False, "{:.2f}x")
        y = self._checkbox(x, y, "Gravitational lensing grid", "gravitational_grid_enabled")
        y = self._slider(x, y, w, "Grid lens strength", "grid_lens_amount",
                         0.0, 10, False, "{:.2f}x")
        y = self._slider(x, y, w, "Grid spacing (screen px)", "grid_target_spacing_px",
                         40.0, 160.0, False, "{:.0f} px")
        
        # === UI ===
        y = self._sec(x, y, "UI")
        y = self._toggle(x, y, w, "Screen mode", "screen_mode", "Light", "Dark", "light", "dark")

        # === ADVANCED / CCD ===
        y = self._sec(x, y, "Advanced (Collisions)")
        y = self._checkbox(x, y, "Enable Adaptive Substeps", "adaptive_substeps")
        y = self._slider(x, y, w, "Substep Precision (+N extra)", "adaptive_substeps_max_extra",
                         0.0, 8.0, False, "+{:.0f} steps")
        y = self._slider(x, y, w, "Force Method Threshold (n)", "force_method_n_threshold",
                 50, 2000, True, "{:.0f} bodies")
        
        # === BUTTONS ===
        y += 20
        bw = (w - 20) // 3
        self.widgets.append(Button(x, y, bw, 35, "Save Config", self.font_sm, self._save))
        self.widgets.append(Button(x + bw + 10, y, bw, 35, "Load Last Config", self.font_sm, self._load))
        self.widgets.append(Button(x + 2*(bw+10), y, bw, 35, "Close (Escape)", self.font_sm, self.toggle))
        
        self.max_scroll = max(0, y + 50 - (self.py + self.ph))
    
    def _sec(self, x, y, txt):
        y += 12
        self.widgets.append(SectionTitle(x, y, txt, self.font_med))
        return y + 26 * state.engine.scale_coefficient
    
    def _checkbox(self, x, y, label, attr):
        self.widgets.append(Checkbox(x, y, label, self.font_sm,
                                     getattr(self.engine, attr),
                                     lambda v: setattr(self.engine, attr, v)))
        return y + 30 * state.engine.scale_coefficient

    def _toggle(self, x, y, w, label, attr, label_a, label_b,
                value_a=False, value_b=True):
        self.widgets.append(Toggle(x, y, w, label, self.font_sm,
                                   getattr(self.engine, attr),
                                   label_a, label_b,
                                   lambda v: setattr(self.engine, attr, v),
                                   value_a, value_b))
        return y + 36 * state.engine.scale_coefficient
    
    def _slider(self, x, y, w, label, attr, mn, mx, log, fmt):
        self.widgets.append(Slider(x, y, w, label, self.font_sm, mn, mx,
                                   getattr(self.engine, attr), log, fmt,
                                   lambda v: setattr(self.engine, attr, v)))
        return y + 60 * state.engine.scale_coefficient
    
    def _save(self):
        cfg = {k: getattr(self.engine, k) for k in [
            # Complete list of parameters shown in the config panel (Physics, Camera, Random, Rendering, UI, Advanced)
            "time_acceleration", 
            "FPS_TARGET", 
            "default_density",
            "fusions", 
            "barnes_hut_theta", 
            "minimum_mass",
            "use_interpolation", 
            "physics_timestep",
            "adaptive_substeps", 
            "adaptive_substeps_max_extra", 
            "force_method_n_threshold",

            "camera_zoom",
            "camera_speed",

            "random_environment_number",
            "random_mode",
            "random_energy_per_kg",
            "random_mass_field",

            "vectors_printed", 
            "force_vectors", 
            "cardinal_vectors",
            "vectors_in_front",
            "vector_scale",
            "vector_time_acceleration_ref",

            "gravitational_grid_enabled", 
            "grid_lens_amount", 
            "grid_target_spacing_px", 
            "grid_max_lines",
            "grid_subdivide_px",
            "grid_lens_softening_world",

            "screen_mode",
     
        ]}
        payload = {
            "version": getattr(self.engine, "project_version", "unknown"),
            "config": cfg,
        }
        try:
            self.engine.fm.create_folder("saves")
            path = self.engine.fm.user_data_path("saves/config.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            setattr(self.engine, "last_saved_config_payload", payload)
            Logger.info(f"Config saved: {path} info: {payload}")
            if hasattr(self.engine, "notify"):
                self.engine.notify("Config saved", duration=2.0)
        except Exception as e:
            Logger.error(f"Save failed: {e}")
    
    def _load(self):
        try:
            path = self.engine.fm.user_data_path("saves/config.json")
            with open(path, 'r') as f:
                raw = json.load(f)
            
            # Handle legacy format (no version) and new format
            if isinstance(raw, dict) and "config" in raw:
                saved_version = raw.get("version")
                cfg = raw.get("config", {})
            else:
                saved_version = None
                cfg = raw

            unknown_keys: list[str] = []
            for k, v in cfg.items():
                if hasattr(self.engine, k):
                    setattr(self.engine, k, v)
                else:
                    unknown_keys.append(k)

            self._build()  # Rebuild UI
            Logger.info(f"Config loaded: {path} info: {raw}")

            # On-screen messages
            if hasattr(self.engine, "notify"):
                if saved_version is not None and saved_version != getattr(self.engine, "project_version", None):
                    self.engine.notify(
                        f"Config v{saved_version} loaded (engine v{self.engine.project_version})",
                        duration=3.0,
                        line=0,
                    )
                else:
                    self.engine.notify("Configuration loaded", duration=2.0, line=0)

                if unknown_keys:
                    self.engine.notify(
                        f"Warning: {len(unknown_keys)} properties not applied (version mismatch?)",
                        duration=4.0,
                        line=1,
                    )
            Logger.info(f"Config loaded: {path}")
        except Exception as e:
            print(f"Load failed: {e}")
            Logger.exception(f"Config load failed: {e}")
            if hasattr(self.engine, "notify"):
                self.engine.notify(f"Config load failed: {e}", duration=4.0, line=1)
    
    def toggle(self):
        Logger.info(f"Config panel toggled: {self.visible}")
        self.visible = not self.visible
        if self.visible:
            self._build()  # Refresh values
    
    def update(self, events):
        if not self.visible:
            return
        
        for e in events:
            # Scroll with mouse wheel when cursor is over the panel
            if e.type == pygame.MOUSEWHEEL:
                if self.panel_rect.collidepoint(pygame.mouse.get_pos()):
                    self.scroll = max(0, min(self.max_scroll, self.scroll - e.y * 20))
            # Scroll with keyboard arrows (global when panel is visible)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.scroll = max(0, self.scroll - 20)
                elif e.key == pygame.K_DOWN:
                    self.scroll = min(self.max_scroll, self.scroll + 20)

        # Update widgets in the same coordinate space as rendering
        for w in self.widgets:
            original_y = w.rect.y
            w.rect.y -= self.scroll
            w.update(events)
            w.rect.y = original_y

    def draw(self):
        if not self.visible:
            return
        
        # Overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(C.OVERLAY)
        self.screen.blit(overlay, (0, 0))
        
        # Panel
        pygame.draw.rect(self.screen, C.PANEL, self.panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, C.TRACK, self.panel_rect, 3, border_radius=10)
        
        # Title area
        title = self.font_big.render("Configuration", True, C.GREEN)
        title_y = self.py + int(20 * state.engine.scale_coefficient)
        self.screen.blit(title, (self.panel_rect.centerx - title.get_width()//2, title_y))
        
        # Line area
        line_y = self.py + int(60 * state.engine.scale_coefficient)
        pygame.draw.line(self.screen, C.TRACK, 
                        (self.px + 25, line_y),
                        (self.px + self.pw - 25, line_y), 2)

        # Définir la zone scrollable pour les widgets — on ne veut pas qu'ils débordent sur le titre ou la barre
        panel_top = self.py + int(70 * state.engine.scale_coefficient)
        panel_bottom = self.py + self.ph

        for w in self.widgets:
            w.rect.y -= self.scroll
            widget_top = w.rect.y
            widget_bottom = w.rect.y + w.rect.height
            # On ne dessine le widget que s'il est entièrement visible DANS LA ZONE SCROLLABLE (en dessous du titre/barre)
            if widget_top >= panel_top and widget_bottom <= panel_bottom:
                w.draw(self.screen)
            w.rect.y += self.scroll