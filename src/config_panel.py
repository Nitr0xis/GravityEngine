"""
Pygame Configuration Panel for Gravity Engine
==============================================

Overlay-style configuration panel with custom widgets.
Press C to open, ESC or click outside to close.

Author: Nils DONTOT
Version: 1.0.0
License: CC BY-NC-SA 4.0
"""

import pygame
import json
import math


# ==================================================================================
# COLORS
# ==================================================================================

class C:
    OVERLAY = (0, 0, 0, 200)
    PANEL = (25, 25, 30)
    SECTION = (35, 35, 40)
    GREEN = (28, 201, 89)
    BLUE = (10, 124, 235)
    WHITE = (255, 255, 255)
    GREY = (180, 180, 180)
    DARK = (100, 100, 100)
    TRACK = (60, 60, 65)


# ==================================================================================
# WIDGETS
# ==================================================================================

class Widget:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.hovered = False
    def update(self, events):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
    def draw(self, surf):
        pass


class Checkbox(Widget):
    def __init__(self, x, y, label, font, val, cb):
        super().__init__(x, y, 20, 20)
        self.label, self.font, self.val, self.cb = label, font, val, cb
        self.anim = 1.0 if val else 0.0
    
    def update(self, events):
        super().update(events)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos):
                self.val = not self.val
                if self.cb: self.cb(self.val)
        self.anim += (( 1.0 if self.val else 0.0) - self.anim) * 0.2
    
    def draw(self, surf):
        pygame.draw.rect(surf, C.SECTION if not self.hovered else (38,221,109), self.rect, border_radius=3)
        pygame.draw.rect(surf, C.TRACK, self.rect, 2, border_radius=3)
        if self.anim > 0.01:
            s = int(12 * self.anim)
            r = pygame.Rect(self.rect.x + (20-s)//2, self.rect.y + (20-s)//2, s, s)
            pygame.draw.rect(surf, C.GREEN, r, border_radius=2)
        txt = self.font.render(self.label, True, C.WHITE)
        surf.blit(txt, (self.rect.x + 30, self.rect.y - 2))


class Slider(Widget):
    def __init__(self, x, y, w, label, font, mn, mx, val, log, fmt, cb):
        super().__init__(x, y, w, 50)
        self.label, self.font, self.mn, self.mx, self.val = label, font, mn, mx, val
        self.log, self.fmt, self.cb = log, fmt, cb
        self.dragging = False
        self._update_pos()
    
    def _update_pos(self):
        if self.log:
            t = (math.log10(self.val) - math.log10(self.mn)) / (math.log10(self.mx) - math.log10(self.mn))
        else:
            t = (self.val - self.mn) / (self.mx - self.mn)
        self.handle_x = self.rect.x + int(t * self.rect.width)
    
    def _val_from_x(self, mx):
        t = max(0, min(1, (mx - self.rect.x) / self.rect.width))
        if self.log:
            lv = math.log10(self.mn) + t * (math.log10(self.mx) - math.log10(self.mn))
            return 10 ** lv
        return self.mn + t * (self.mx - self.mn)
    
    def update(self, events):
        super().update(events)
        mx = pygame.mouse.get_pos()[0]
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                track_r = pygame.Rect(self.rect.x, self.rect.y + 25, self.rect.width, 10)
                if track_r.collidepoint(e.pos):
                    self.dragging = True
                    self.val = self._val_from_x(mx)
                    self._update_pos()
                    if self.cb: self.cb(self.val)
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.dragging = False
            elif e.type == pygame.MOUSEMOTION and self.dragging:
                self.val = self._val_from_x(mx)
                self._update_pos()
                if self.cb: self.cb(self.val)
    
    def draw(self, surf):
        # Label
        txt = self.font.render(self.label, True, C.WHITE)
        surf.blit(txt, (self.rect.x, self.rect.y))
        # Value
        val_txt = self.font.render(self.fmt.format(self.val), True, C.GREEN)
        surf.blit(val_txt, (self.rect.right - val_txt.get_width(), self.rect.y))
        # Track
        track_r = pygame.Rect(self.rect.x, self.rect.y + 25, self.rect.width, 6)
        pygame.draw.rect(surf, C.TRACK, track_r, border_radius=3)
        # Fill
        if self.handle_x > self.rect.x:
            fill_r = pygame.Rect(self.rect.x, self.rect.y + 25, self.handle_x - self.rect.x, 6)
            pygame.draw.rect(surf, C.GREEN, fill_r, border_radius=3)
        # Handle
        col = (38,221,109) if self.hovered or self.dragging else C.GREEN
        pygame.draw.circle(surf, col, (self.handle_x, self.rect.y + 28), 8)


class Button(Widget):
    def __init__(self, x, y, w, h, text, font, cb):
        super().__init__(x, y, w, h)
        self.text, self.font, self.cb = text, font, cb
    
    def update(self, events):
        super().update(events)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos):
                if self.cb: self.cb()
    
    def draw(self, surf):
        col = (38,221,109) if self.hovered else C.SECTION
        pygame.draw.rect(surf, col, self.rect, border_radius=5)
        pygame.draw.rect(surf, C.TRACK, self.rect, 2, border_radius=5)
        txt = self.font.render(self.text, True, C.WHITE)
        surf.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))


# ==================================================================================
# MAIN PANEL
# ==================================================================================

class ConfigPanel:
    def __init__(self, engine, screen, font_path):
        self.engine, self.screen = engine, screen
        self.font_big = pygame.font.Font(font_path, 28)
        self.font_med = pygame.font.Font(font_path, 20)
        self.font_sm = pygame.font.Font(font_path, 16)
        
        self.visible = False
        self.widgets = []
        
        # Panel rect
        self.pw, self.ph = 650, 750
        self.px = (screen.get_width() - self.pw) // 2
        self.py = (screen.get_height() - self.ph) // 2
        self.panel_rect = pygame.Rect(self.px, self.py, self.pw, self.ph)
        
        # Scroll
        self.scroll = 0
        self.max_scroll = 0
        
        self._build()
    
    def _build(self):
        self.widgets.clear()
        x, y = self.px + 25, self.py + 70
        w = self.pw - 50
        
        # === SIMULATION ===
        y = self._sec(x, y, "Simulation")
        y = self._slider(x, y, w, "Target FPS", "FPS_TARGET",
                         30, 240, False, "{:.0f} FPS")
        y = self._slider(x, y, w, "Time Acceleration", "time_acceleration",
                         1e3, 1e8, True, "{:.2e}x")
        
        # === PHYSICS ===
        y = self._sec(x, y, "Physics")
        y = self._checkbox(x, y, "Enable Reversed Gravity", "reversed_gravity")
        y = self._checkbox(x, y, "Enable Random Speed Mode", "random_mode")
        y = self._slider(x, y, w, "Corpses Density", "default_density",
                         1e2, 1e9, True, "{:.2e} kg/m³")  # 1e9 is the average density of white dwarfs
        y = self._checkbox(x, y, "Enable Body Fusions", "fusions")
        
        # === VISUAL ===
        y = self._sec(x, y, "Visual")
        y = self._slider(x, y, w, "Camera Zoom", "camera_zoom",
                         1e-7, 100.0, True, "{:.2e}x")
        y = self._checkbox(x, y, "Show Vectors", "vectors_printed")
        y = self._slider(x, y, w, "Vector Scale", "vector_scale",
                         0.1, 10.0, False, "{:.2f}x")

        # === ADVANCED / CCD ===
        y = self._sec(x, y, "Advanced (Collisions)")
        y = self._checkbox(x, y, "Enable Adaptive Substeps", "adaptive_substeps")
        y = self._slider(x, y, w, "Substep Precision (+N extra)", "adaptive_substeps_max_extra",
                         0.0, 8.0, False, "+{:.0f} steps")
        
        # === BUTTONS ===
        y += 20
        bw = (w - 20) // 3
        self.widgets.append(Button(x, y, bw, 35, "Save Config", self.font_sm, self._save))
        self.widgets.append(Button(x + bw + 10, y, bw, 35, "Load Last Config", self.font_sm, self._load))
        self.widgets.append(Button(x + 2*(bw+10), y, bw, 35, "Close (Escape)", self.font_sm, self.toggle))
        
        self.max_scroll = max(0, y + 50 - (self.py + self.ph))
    
    def _sec(self, x, y, txt):
        y += 15
        return y + 30
    
    def _checkbox(self, x, y, label, attr):
        self.widgets.append(Checkbox(x, y, label, self.font_sm,
                                     getattr(self.engine, attr),
                                     lambda v: setattr(self.engine, attr, v)))
        return y + 30
    
    def _slider(self, x, y, w, label, attr, mn, mx, log, fmt):
        self.widgets.append(Slider(x, y, w, label, self.font_sm, mn, mx,
                                   getattr(self.engine, attr), log, fmt,
                                   lambda v: setattr(self.engine, attr, v)))
        return y + 60
    
    def _save(self):
        cfg = {k: getattr(self.engine, k) for k in [
            "time_acceleration", "FPS_TARGET", "default_density", "fusions",
            "vectors_printed", "force_vectors", "vector_scale", "camera_zoom",
            "adaptive_substeps", "adaptive_substeps_max_extra"
        ]}
        payload = {
            "version": getattr(self.engine, "project_version", "unknown"),
            "config": cfg,
        }
        try:
            path = self.engine.fm.user_data_path("saves/config.json")
            with open(path, 'w') as f:
                json.dump(payload, f, indent=2)
            print(f"✓ Config saved: {path}")
            # On-screen message
            if hasattr(self.engine, "notify"):
                self.engine.notify("Configuration saved", duration=2.0)
        except Exception as e:
            print(f"✗ Save failed: {e}")
    
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
            print(f"✓ Config loaded: {path}")

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
        except Exception as e:
            print(f"✗ Load failed: {e}")
    
    def toggle(self):
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
        
        # Title
        title = self.font_big.render("Configuration", True, C.GREEN)
        self.screen.blit(title, (self.panel_rect.centerx - title.get_width()//2, self.py + 20))
        
        # Line
        pygame.draw.line(self.screen, C.TRACK, 
                        (self.px + 25, self.py + 60),
                        (self.px + self.pw - 25, self.py + 60), 2)
        
        # Widgets (with scroll)
        for w in self.widgets:
            w.rect.y -= self.scroll
            if self.py < w.rect.y < self.py + self.ph:
                w.draw(self.screen)
            w.rect.y += self.scroll
            