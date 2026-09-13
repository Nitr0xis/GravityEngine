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
Base UI widgets shared across the project (config panel, in-game buttons, etc.).

Any new UI element (config panel controls, HUD buttons, future overlays)
should be built from the primitives defined here, rather than redefining
its own drawing/interaction logic — keeps visual style and event handling
consistent across the whole app.
"""

import math
import pygame

from core import state


class C:
    OVERLAY = (0, 0, 0, 100)
    PANEL = (25, 25, 30)
    SECTION = (35, 35, 40)
    GREEN = (28, 201, 89)
    BLUE = (10, 124, 235)
    WHITE = (255, 255, 255)
    GREY = (180, 180, 180)
    DARK = (100, 100, 100)
    TRACK = (60, 60, 65)


class Widget:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.hovered = False

    def update(self, events):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, surf):
        pass


class SectionTitle(Widget):
    """Section title (text only, non-interactive, scaled)."""

    def __init__(self, x, y, text, font):
        scale = state.engine.scale_coefficient
        font_height = int(22 * scale)
        super().__init__(x, y, 1, font_height)
        self.text = text
        self.font = font
        self._scale = scale  # keep in case padding adjustment is needed later

    def update(self, events):
        pass

    def draw(self, surf):
        scale = state.engine.scale_coefficient
        t = self.font.render(self.text, True, C.BLUE)
        surf.blit(t, (self.rect.x, self.rect.y))


class Checkbox(Widget):
    def __init__(self, x, y, label, font, val, cb):
        scale = state.engine.scale_coefficient
        size = int(20 * scale)
        super().__init__(x, y, size, size)
        self.label, self.font, self.val, self.cb = label, font, val, cb
        self.anim = 1.0 if val else 0.0
        self._scale = scale  # store the scale for use in draw

    def update(self, events):
        super().update(events)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos):
                self.val = not self.val
                if self.cb:
                    self.cb(self.val)
        self.anim += ((1.0 if self.val else 0.0) - self.anim) * 0.2

    def draw(self, surf):
        scale = state.engine.scale_coefficient
        main_size = int(20 * scale)
        inner_size = int(12 * scale * self.anim)
        base_x, base_y = self.rect.x, self.rect.y

        rect = pygame.Rect(base_x, base_y, main_size, main_size)
        pygame.draw.rect(
            surf, C.SECTION if not self.hovered else (38, 221, 109),
            rect, border_radius=int(3 * scale)
        )
        pygame.draw.rect(
            surf, C.TRACK, rect, int(2 * scale), border_radius=int(3 * scale)
        )
        if self.anim > 0.01:
            s = inner_size
            r = pygame.Rect(
                base_x + (main_size - s) // 2,
                base_y + (main_size - s) // 2,
                s,
                s,
            )
            pygame.draw.rect(surf, C.GREEN, r, border_radius=int(2 * scale))
        txt = self.font.render(self.label, True, C.WHITE)
        # offset the text proportionally to scale
        surf.blit(txt, (base_x + int(30 * scale), base_y - int(2 * scale)))


class Toggle(Widget):
    """Two-option selector. Values default to False / True but can be any type."""

    def __init__(self, x, y, w, label, font, val, label_a, label_b, cb,
                 value_a=False, value_b=True):
        # The base dimensions are multiplied by the scale_coefficient
        scale = state.engine.scale_coefficient
        base_height = 28
        scaled_height = int(base_height * scale)
        super().__init__(x, y, w, scaled_height)
        self.label, self.font, self.val = label, font, val
        self.label_a, self.label_b, self.cb = label_a, label_b, cb
        self.value_a, self.value_b = value_a, value_b
        self._a_rect = pygame.Rect(0, 0, 1, 1)
        self._b_rect = pygame.Rect(0, 0, 1, 1)
        self._scale = scale  # store for use in _layout, etc.

    def _layout(self):
        scale = state.engine.scale_coefficient
        pad = int(8 * scale)
        gap = int(6 * scale)
        option_h = int(24 * scale)
        label_surf = self.font.render(self.label, True, C.WHITE)
        opt_y = self.rect.y + (self.rect.height - option_h) // 2
        opt_x = self.rect.x + label_surf.get_width() + pad
        # Minimum width also scaled
        min_opt_w = int(40 * scale)
        opt_w_full = (self.rect.right - opt_x - gap)
        opt_w = max(min_opt_w, opt_w_full // 2)
        # Correction: make sure opt_w is never negative
        if opt_w_full < 0:
            opt_w = min_opt_w
        self._a_rect = pygame.Rect(opt_x, opt_y, opt_w, option_h)
        self._b_rect = pygame.Rect(opt_x + opt_w + gap, opt_y, opt_w, option_h)

    def update(self, events):
        self._layout()
        mx, my = pygame.mouse.get_pos()
        self.hovered = self._a_rect.collidepoint(mx, my) or self._b_rect.collidepoint(mx, my)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self._a_rect.collidepoint(e.pos):
                    self.val = self.value_a
                    if self.cb:
                        self.cb(self.val)
                elif self._b_rect.collidepoint(e.pos):
                    self.val = self.value_b
                    if self.cb:
                        self.cb(self.val)

    def draw(self, surf):
        self._layout()
        scale = state.engine.scale_coefficient
        txt = self.font.render(self.label, True, C.WHITE)
        surf.blit(txt, (self.rect.x, self.rect.y + (self.rect.height - txt.get_height()) // 2))
        mx, my = pygame.mouse.get_pos()
        border_radius = int(5 * scale)
        for rect, selected, text in (
            (self._a_rect, self.val == self.value_a, self.label_a),
            (self._b_rect, self.val == self.value_b, self.label_b),
        ):
            hover = rect.collidepoint(mx, my)
            fill = C.GREEN if selected else ((38, 221, 109) if hover else C.SECTION)
            pygame.draw.rect(surf, fill, rect, border_radius=border_radius)
            pygame.draw.rect(surf, C.TRACK, rect, 2, border_radius=border_radius)
            t = self.font.render(text, True, C.WHITE)
            surf.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))


class Slider(Widget):
    def __init__(self, x, y, w, label, font, mn, mx, val, log, fmt, cb):
        # Height dynamically scaled with the coefficient
        super().__init__(x, y, w, int(50 * state.engine.scale_coefficient))
        self.label = label
        self.font = font
        self.mn = mn
        self.mx = mx
        self.val = val
        self.log = log
        self.fmt = fmt
        self.cb = cb
        self.dragging = False
        self._update_pos()

    def _update_pos(self):
        if self.log:
            if self.val <= 0 or self.mn <= 0 or self.mx <= 0:
                t = 0.0
            else:
                try:
                    t = (math.log10(self.val) - math.log10(self.mn)) / (math.log10(self.mx) - math.log10(self.mn))
                except ZeroDivisionError:
                    t = 0.0
        else:
            try:
                t = (self.val - self.mn) / (self.mx - self.mn)
            except ZeroDivisionError:
                t = 0.0
        t = max(0.0, min(1.0, t))
        self.handle_x = self.rect.x + int(t * self.rect.width)

    def _val_from_x(self, mx):
        t = max(0, min(1, (mx - self.rect.x) / self.rect.width)) if self.rect.width != 0 else 0
        if self.log:
            if self.mn <= 0 or self.mx <= 0:
                return self.mn
            lv = math.log10(self.mn) + t * (math.log10(self.mx) - math.log10(self.mn))
            return 10 ** lv
        return self.mn + t * (self.mx - self.mn)

    def _hit_test(self, pos):
        """
        Enlarged clickable zone: the track (a bar higher than before)
        OR a generous circle around the cursor — covers both natural ways
        to aim at the slider (clicking on the line, or aiming directly at
        the handle).
        """
        px, py = pos
        # Track height and vertical placement adapted to scale_coefficient
        scale = state.engine.scale_coefficient
        track_height = int(24 * scale)
        track_y = self.rect.y + int((25 - 7) * scale)
        track_r = pygame.Rect(self.rect.x, track_y, self.rect.width, track_height)
        if track_r.collidepoint(pos):
            return True
        # Tolerance circle around the handle, wider than its visual radius (8px)
        # The radius is also adapted to the scale_coefficient
        handle_center = (self.handle_x, self.rect.y + int(28 * scale))
        dist = math.hypot(px - handle_center[0], py - handle_center[1])
        return dist <= int(16 * scale)

    def update(self, events):
        super().update(events)
        mx = pygame.mouse.get_pos()[0]
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self._hit_test(e.pos):
                    self.dragging = True
                    self.val = self._val_from_x(mx)
                    self._update_pos()
                    if self.cb:
                        self.cb(self.val)
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.dragging = False
            elif e.type == pygame.MOUSEMOTION and self.dragging:
                self.val = self._val_from_x(mx)
                self._update_pos()
                if self.cb:
                    self.cb(self.val)

    def draw(self, surf):
        scale = state.engine.scale_coefficient
        txt = self.font.render(self.label, True, C.WHITE)
        surf.blit(txt, (self.rect.x, self.rect.y))
        val_txt = self.font.render(self.fmt.format(self.val), True, C.GREEN)
        surf.blit(val_txt, (self.rect.right - val_txt.get_width(), self.rect.y))

        # Track height and placement adapted
        track_y = self.rect.y + int(25 * scale)
        track_height = int(6 * scale)
        track_r = pygame.Rect(self.rect.x, track_y, self.rect.width, track_height)
        pygame.draw.rect(surf, C.TRACK, track_r, border_radius=int(3 * scale))
        if self.handle_x > self.rect.x:
            fill_r = pygame.Rect(self.rect.x, track_y, self.handle_x - self.rect.x, track_height)
            pygame.draw.rect(surf, C.GREEN, fill_r, border_radius=int(3 * scale))
        col = (38, 221, 109) if self.hovered or self.dragging else C.GREEN
        handle_radius = int(8 * scale)
        pygame.draw.circle(surf, col, (self.handle_x, self.rect.y + int(28 * scale)), handle_radius)


class Button(Widget):
    def __init__(self, x, y, w, h, text, font, cb, visible_if=None):
        super().__init__(x, y, w, h)
        self.text = text
        self.font = font
        self.cb = cb
        self.visible_if = visible_if

    def is_visible(self):
        return self.visible_if is None or bool(self.visible_if())

    def update(self, events):
        if not self.is_visible():
            self.hovered = False
            return
        super().update(events)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos):
                if self.cb:
                    self.cb()

    def draw(self, surf):
        if not self.is_visible():
            return
        scale = state.engine.scale_coefficient
        border_radius = int(5 * scale)
        border_width = max(int(2 * scale), 1)
        col = (38, 221, 109) if self.hovered else C.SECTION
        pygame.draw.rect(surf, col, self.rect, border_radius=border_radius)
        pygame.draw.rect(surf, C.TRACK, self.rect, border_width, border_radius=border_radius)
        txt = self.font.render(self.text, True, C.WHITE)
        surf.blit(
            txt,
            (
                self.rect.centerx - txt.get_width() // 2,
                self.rect.centery - txt.get_height() // 2
            )
        )
