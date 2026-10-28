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
import time

from core.logger import Logger
from core import state
from rendering.ui_widgets import (
    C, Widget, SectionTitle, Checkbox, Toggle, Slider, Button, TextInput
)


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
        self._hover_widget = None
        self._hover_since = None
        self._mouse_pressed = False
        self.body_number_input = None

        # Save
        self._build_param_keys = []
        
        self._build()
    
    def _build(self):
        self.widgets.clear()
        # Space left at the top for the title and bar — must be synchronized with draw() below
        y_offset_top = int(70 * state.engine.scale_coefficient)
        x, y = self.px + 25, self.py + y_offset_top
        w = (self.pw - 50)

        # Keep the list of all parameters actually present in the panel, in order
        self._build_param_keys = []

        # === SIMULATION ===
        y = self._sec(x, y, "Simulation")
        y = self._slider(x, y, w, "Target FPS", "FPS_TARGET",
                         30, 240, False, "{:.0f} FPS",
                         "Sets the target frame rate for the simulation.")
        y = self._slider(x, y, w, "Time Acceleration", "time_acceleration",
                         1e0, 5e5, True, "{:.2e}x",
                         "Changes the speed of simulated time relative to real time.")

        # === PHYSICS ===
        y = self._sec(x, y, "Physics")
        y = self._checkbox(x, y, "Enable Reversed Gravity", "reversed_gravity",
                           "Reverses gravitational attraction into repulsion.")
        y = self._checkbox(x, y, "Enable Random Speed Mode", "random_mode",
                           "Gives newly created bodies a random velocity.")
        y = self._slider(x, y, w, "Bodies Density", "default_density",
                         1e0, 1e5, True, "{:.2e} kg/m³",
                         "Sets the density of newly created bodies.")
        y = self._checkbox(x, y, "Enable Body Fusions", "fusions",
                           "Allows bodies to absorb smaller bodies on collision.")
        y = self._slider(x, y, w, "Barnes-Hut Theta", "barnes_hut_theta",
                 0.0, 1.5, False, "{:.2f}",
                 "Adjusts the accuracy and speed of the Barnes-Hut calculation.")
        y = self._slider(x, y, w, "Random-Generated Bodies Count", "random_environment_number",
                 1, 200, False, "{:.0f} bodies",
                 "Sets the number of bodies created when generating an environment.")

        # === VISUAL ===
        y = self._sec(x, y, "Visual")

        # = Camera Zoom Specifications =
        self.widgets.append(Slider(x, y, w, "Camera Zoom", self.font_sm,
                            self.engine.camera.min_scale, self.engine.camera.max_scale,
                            self.engine.camera.scale, True, "{:.2e}x",
                            self._on_zoom_slider,
                            "Adjusts the camera zoom level."))
        self._build_param_keys.append("camera_zoom")
        y += 60 * state.engine.scale_coefficient
        # = = = = = = = = = = = = = = =

        y = self._checkbox(x, y, "Show Vectors", "vectors_printed",
                           "Displays each body's velocity and force vectors.")
        y = self._slider(x, y, w, "Vector Scale", "vector_scale",
                         0.1, 10.0, False, "{:.1f}×",
                         "Adjusts the size of the displayed vectors.")
        y = self._checkbox(x, y, "Gravitational Lensing Grid", "gravitational_grid_enabled",
                           "Displays a grid that visualizes gravitational lensing.")
        y = self._slider(x, y, w, "Grid Lens Strength", "grid_lens_amount",
                         0.0, 10.0, False, "{:.1f}×",
                         "Adjusts the strength of the grid's deformation.")
        y = self._slider(x, y, w, "Grid Spacing (screen px)", "grid_target_spacing_px",
                         40.0, 160.0, False, "{:.0f} px",
                         "Adjusts the grid spacing in screen pixels.")

        # === UI ===
        y = self._sec(x, y, "UI")
        y = self._toggle(x, y, w, "Screen mode", "screen_mode", "Light", "Dark", "light", "dark",
                         help_text="Chooses the light or dark interface theme.")
        """y = self._slider(x, y, w, "UI scale", "scale_coefficient", 0.5, 4.0, True, "{:.1f}×"); self._build_param_keys.append("scale_coefficient")"""

        # === BODY SELECTION ===
        y = self._sec(x, y, "Body Selection")
        scale = state.engine.scale_coefficient
        select_button_w = int(95 * scale)
        input_gap = int(10 * scale)
        input_w = w - select_button_w - input_gap
        self.body_number_input = TextInput(
            x, y, input_w, "Body number", self.font_sm,
            self._select_body_by_number,
            "Enter a body number, then press Enter or click Select."
        )
        self.widgets.append(self.body_number_input)
        self.widgets.append(Button(
            x + input_w + input_gap, y + int(20 * scale),
            select_button_w, int(32 * scale), "Select", self.font_sm,
            self._submit_body_number,
            help_text="Selects the body with the entered number."
        ))
        y += 79 * scale
   
        # === ADVANCED / CCD ===
        y = self._sec(x, y, "Advanced (Collisions)")
        y = self._checkbox(x, y, "Enable Adaptive Substeps", "adaptive_substeps",
                           "Splits physics steps into substeps to better handle fast-moving bodies.")
        y = self._slider(x, y, w, "Substep Precision (+N extra)", "adaptive_substeps_max_extra",
                         0.0, 8.0, False, "+{:.0f} steps",
                         "Sets the maximum number of additional adaptive substeps.")
        y = self._slider(x, y, w, "Force Method Threshold (n)", "force_method_n_threshold",
                 50, 2000, True, "{:.0f} bodies",
                 "Sets the body count threshold for using the Barnes-Hut method.")

        # === BUTTONS ===
        y += int(20 * state.engine.scale_coefficient)
        scale = state.engine.scale_coefficient
        gap = int(10 * scale)
        bw = (w - 2 * gap) // 3  # w est déjà la largeur du panneau, déjà cohérente
        button_h = int(35 * scale)

        self.widgets.append(Button(
            x, y, bw, button_h, "Save Config", self.font_sm, self._save,
            help_text="Saves the current settings to the configuration file."
        ))
        self.widgets.append(Button(
            x + bw + gap, y, bw, button_h, "Load Last Config", self.font_sm, self._load,
            help_text="Loads the most recently saved settings."
        ))
        self.widgets.append(Button(
            x + 2 * (bw + gap), y, bw, button_h, "Close (Escape)", self.font_sm, self.toggle,
            help_text="Closes the configuration panel."
        ))

        margin = button_h + int(20 * scale)
        self.max_scroll = max(0, int(y + margin - (self.py + self.ph)))
        self.scroll = max(0, min(self.scroll, self.max_scroll))

    def _sec(self, x, y, txt):
        y += 12
        self.widgets.append(SectionTitle(x, y, txt, self.font_med))
        return y + 26 * state.engine.scale_coefficient

    def _checkbox(self, x, y, label, attr, help_text=""):
        self.widgets.append(Checkbox(x, y, label, self.font_sm,
                                     getattr(self.engine, attr),
                                     lambda v: setattr(self.engine, attr, v),
                                     help_text))
        self._build_param_keys.append(attr)
        return y + 30 * state.engine.scale_coefficient

    def _toggle(self, x, y, w, label, attr, label_a, label_b,
                value_a=False, value_b=True, help_text=""):
        self.widgets.append(Toggle(x, y, w, label, self.font_sm,
                                   getattr(self.engine, attr),
                                   label_a, label_b,
                                   lambda v: setattr(self.engine, attr, v),
                                   value_a, value_b, help_text))
        self._build_param_keys.append(attr)
        return y + 36 * state.engine.scale_coefficient

    def _slider(self, x, y, w, label, attr, mn, mx, log, fmt, help_text=""):
        self.widgets.append(Slider(x, y, w, label, self.font_sm, mn, mx,
                                   getattr(self.engine, attr), log, fmt,
                                   lambda v: setattr(self.engine, attr, v),
                                   help_text))
        self._build_param_keys.append(attr)
        return y + 60 * state.engine.scale_coefficient

    def _select_body_by_number(self, number_text: str) -> None:
        if self.body_number_input is None:
            return
        if not number_text:
            self.body_number_input.error = "Enter a body number."
            return
        number = int(number_text)
        if not any(circle.number == number for circle in state.circles):
            self.body_number_input.error = f"Body number {number} does not exist."
            return
        self.engine.select_circle(number)
        self.body_number_input.error = ""

    def _submit_body_number(self) -> None:
        if self.body_number_input is not None:
            self._select_body_by_number(self.body_number_input.value)

    @property
    def has_keyboard_focus(self) -> bool:
        return (
            self.body_number_input is not None
            and self.body_number_input.focused
        )

    def _on_zoom_slider(self, v):
        screen_center = (state.engine.screen.get_width() // 2, state.engine.screen.get_height() // 2)
        state.engine.camera.set_scale_anchored(v, screen_center)

    def _save(self):
        # Only the parameters actually present in the panel are saved
        # We use self._build_param_keys, which is generated during the last _build
        param_keys = getattr(self, "_build_param_keys", [])
        cfg = {k: getattr(self.engine, k) for k in param_keys}
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
        elif self.body_number_input is not None:
            self.body_number_input._set_focus(False)
            self._hover_widget = None
            self._hover_since = None
            self._mouse_pressed = False

    def _visible_help_widget(self, widget):
        if not widget.help_text or not widget.hovered:
            return False
        panel_top = self.py + int(70 * state.engine.scale_coefficient)
        widget_top = widget.rect.top - self.scroll
        widget_bottom = widget.rect.bottom - self.scroll
        return (
            self.panel_rect.collidepoint(pygame.mouse.get_pos())
            and widget_top >= panel_top
            and widget_bottom <= self.panel_rect.bottom
        )

    def _set_scroll(self, value):
        self.scroll = max(0, min(int(value), self.max_scroll))

    def update(self, events):
        if not self.visible:
            return

        self._set_scroll(self.scroll)
        
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_pressed = True
            elif e.type == pygame.MOUSEBUTTONUP:
                self._mouse_pressed = False

            # Scroll with mouse wheel when cursor is over the panel
            if e.type == pygame.MOUSEWHEEL:
                if self.panel_rect.collidepoint(pygame.mouse.get_pos()):
                    self._set_scroll(self.scroll - e.y * 20)
            # Scroll with keyboard arrows (global when panel is visible)
            elif e.type == pygame.KEYDOWN:
                if not self.has_keyboard_focus:
                    if e.key == pygame.K_UP:
                        self._set_scroll(self.scroll - 20)
                    elif e.key == pygame.K_DOWN:
                        self._set_scroll(self.scroll + 20)

        # Update widgets in the same coordinate space as rendering
        for w in self.widgets:
            original_y = w.rect.y
            hover_original_y = w.hover_rect.y
            try:
                w.rect.y -= self.scroll
                w.hover_rect.y -= self.scroll
                w.update(events)
            finally:
                w.rect.y = original_y
                w.hover_rect.y = hover_original_y

        if not self.visible:
            self._hover_widget = None
            self._hover_since = None
            self._mouse_pressed = False
            return

        hovered = next(
            (
                widget for widget in reversed(self.widgets)
                if self._visible_help_widget(widget)
            ),
            None,
        )
        if self._mouse_pressed or hovered is None:
            self._hover_widget = None
            self._hover_since = None
        elif hovered is not self._hover_widget:
            self._hover_widget = hovered
            self._hover_since = time.monotonic()

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

        # Define the scrollable area for widgets — we don't want them to overflow over the title or bar
        panel_top = self.py + int(70 * state.engine.scale_coefficient)
        panel_bottom = self.py + self.ph
        content_clip = pygame.Rect(
            self.px,
            panel_top,
            self.pw,
            panel_bottom - panel_top,
        )

        previous_clip = self.screen.get_clip()
        self.screen.set_clip(content_clip)
        try:
            for w in self.widgets:
                original_y = w.rect.y
                try:
                    w.rect.y -= self.scroll
                    if w.rect.colliderect(content_clip):
                        w.draw(self.screen)
                finally:
                    w.rect.y = original_y
        finally:
            self.screen.set_clip(previous_clip)

        if (
            self._hover_widget is not None
            and self._hover_since is not None
            and not self._mouse_pressed
            and time.monotonic() - self._hover_since >= 0.5
        ):
            self._draw_helpbox(self._hover_widget.help_text)

    def _draw_helpbox(self, text):
        scale = state.engine.scale_coefficient
        padding = int(8 * scale)
        max_width = int(300 * scale)
        lines = []
        current_line = ""
        for word in text.split():
            candidate = f"{current_line} {word}".strip()
            if current_line and self.font_sm.size(candidate)[0] > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = candidate
        if current_line:
            lines.append(current_line)

        rendered_lines = [
            self.font_sm.render(line, True, C.WHITE)
            for line in lines
        ]
        content_width = max((line.get_width() for line in rendered_lines), default=0)
        line_height = self.font_sm.get_linesize()
        box = pygame.Rect(
            0, 0,
            content_width + 2 * padding,
            len(rendered_lines) * line_height + 2 * padding
        )
        mx, my = pygame.mouse.get_pos()
        box.x = mx + int(16 * scale)
        box.y = my + int(18 * scale)
        margin = int(6 * scale)
        box.x = max(
            margin,
            min(box.x, self.screen.get_width() - margin - box.width)
        )
        box.y = max(
            margin,
            min(box.y, self.screen.get_height() - margin - box.height)
        )

        pygame.draw.rect(self.screen, (0, 0, 0), box, border_radius=int(3 * scale))
        pygame.draw.rect(
            self.screen, (125, 125, 130), box, max(1, int(scale)),
            border_radius=int(3 * scale)
        )
        for index, line in enumerate(rendered_lines):
            self.screen.blit(
                line,
                (box.x + padding, box.y + padding + index * line_height)
            )
            