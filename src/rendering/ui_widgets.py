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
    OVERLAY = (0, 0, 0, 200)
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
    """Titre de section (texte seul, non interactif)."""

    def __init__(self, x, y, text, font):
        super().__init__(x, y, 1, 22)
        self.text = text
        self.font = font

    def update(self, events):
        pass

    def draw(self, surf):
        t = self.font.render(self.text, True, C.BLUE)
        surf.blit(t, (self.rect.x, self.rect.y))


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
        self.anim += ((1.0 if self.val else 0.0) - self.anim) * 0.2

    def draw(self, surf):
        pygame.draw.rect(surf, C.SECTION if not self.hovered else (38, 221, 109), self.rect, border_radius=3)
        pygame.draw.rect(surf, C.TRACK, self.rect, 2, border_radius=3)
        if self.anim > 0.01:
            s = int(12 * self.anim)
            r = pygame.Rect(self.rect.x + (20 - s) // 2, self.rect.y + (20 - s) // 2, s, s)
            pygame.draw.rect(surf, C.GREEN, r, border_radius=2)
        txt = self.font.render(self.label, True, C.WHITE)
        surf.blit(txt, (self.rect.x + 30, self.rect.y - 2))


class Toggle(Widget):
    """Two-option selector. Values default to False / True but can be any type."""

    def __init__(self, x, y, w, label, font, val, label_a, label_b, cb,
                 value_a=False, value_b=True):
        super().__init__(x, y, w, 28)
        self.label, self.font, self.val = label, font, val
        self.label_a, self.label_b, self.cb = label_a, label_b, cb
        self.value_a, self.value_b = value_a, value_b
        self._a_rect = pygame.Rect(0, 0, 1, 1)
        self._b_rect = pygame.Rect(0, 0, 1, 1)

    def _layout(self):
        pad = 8
        gap = 6
        option_h = 24
        label_surf = self.font.render(self.label, True, C.WHITE)
        opt_y = self.rect.y + (self.rect.height - option_h) // 2
        opt_x = self.rect.x + label_surf.get_width() + pad
        opt_w = max(40, (self.rect.right - opt_x - gap) // 2)
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
                    if self.cb: self.cb(self.val)
                elif self._b_rect.collidepoint(e.pos):
                    self.val = self.value_b
                    if self.cb: self.cb(self.val)

    def draw(self, surf):
        self._layout()
        txt = self.font.render(self.label, True, C.WHITE)
        surf.blit(txt, (self.rect.x, self.rect.y + (self.rect.height - txt.get_height()) // 2))
        mx, my = pygame.mouse.get_pos()
        for rect, selected, text in (
            (self._a_rect, self.val == self.value_a, self.label_a),
            (self._b_rect, self.val == self.value_b, self.label_b),
        ):
            hover = rect.collidepoint(mx, my)
            fill = C.GREEN if selected else ((38, 221, 109) if hover else C.SECTION)
            pygame.draw.rect(surf, fill, rect, border_radius=5)
            pygame.draw.rect(surf, C.TRACK, rect, 2, border_radius=5)
            t = self.font.render(text, True, C.WHITE)
            surf.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))


class Slider(Widget):
    def __init__(self, x, y, w, label, font, mn, mx, val, log, fmt, cb):
        super().__init__(x, y, w, 50)
        self.label, self.font, self.mn, self.mx, self.val = label, font, mn, mx, val
        self.log, self.fmt, self.cb = log, fmt, cb
        self.dragging = False
        self._update_pos()

    def _update_pos(self):
        # Clamp value to bounds before calculating position
        self.val = min(max(self.val, self.mn), self.mx)
        if self.log:
            t = (math.log10(self.val) - math.log10(self.mn)) / (math.log10(self.mx) - math.log10(self.mn))
        else:
            t = (self.val - self.mn) / (self.mx - self.mn)
        t = min(max(t, 0), 1)
        self.handle_x = self.rect.x + int(t * self.rect.width)

    def _val_from_x(self, mx):
        t = max(0, min(1, (mx - self.rect.x) / self.rect.width))
        if self.log:
            lv = math.log10(self.mn) + t * (math.log10(self.mx) - math.log10(self.mn))
            return 10 ** lv
        return self.mn + t * (self.mx - self.mn)

    def update(self, events):
        super().update(events)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Correction: calculer dynamiquement la zone du slider (barre)
                track_r = pygame.Rect(self.rect.x, self.rect.y + int(25 * state.engine.scale_coefficient), self.rect.width, 6)
                if track_r.collidepoint(e.pos):
                    self.dragging = True
                    self.val = self._val_from_x(e.pos[0])
                    self._update_pos()
                    if self.cb: self.cb(self.val)
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.dragging = False
            elif e.type == pygame.MOUSEMOTION and self.dragging:
                self.val = self._val_from_x(e.pos[0])
                self._update_pos()
                if self.cb: self.cb(self.val)

    def draw(self, surf):
        txt = self.font.render(self.label, True, C.WHITE)
        surf.blit(txt, (self.rect.x, self.rect.y))
        val_txt = self.font.render(self.fmt.format(self.val), True, C.GREEN)
        surf.blit(val_txt, (self.rect.right - val_txt.get_width(), self.rect.y))
        track_r = pygame.Rect(self.rect.x, self.rect.y + int(25 * state.engine.scale_coefficient), self.rect.width, 6)
        pygame.draw.rect(surf, C.TRACK, track_r, border_radius=3)
        if self.handle_x > self.rect.x:
            fill_r = pygame.Rect(self.rect.x, self.rect.y + int(25 * state.engine.scale_coefficient), self.handle_x - self.rect.x, 6)
            pygame.draw.rect(surf, C.GREEN, fill_r, border_radius=3)
        col = (38, 221, 109) if self.hovered or self.dragging else C.GREEN
        pygame.draw.circle(surf, col, (self.handle_x, self.rect.y + int(28 * state.engine.scale_coefficient)), 8)


class Button(Widget):
    def __init__(self, x, y, w, h, text, font, cb, visible_if=None):
        super().__init__(x, y, w, h)
        self.text, self.font, self.cb = text, font, cb
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
                if self.cb: self.cb()

    def draw(self, surf):
        if not self.is_visible():
            return
        col = (38, 221, 109) if self.hovered else C.SECTION
        pygame.draw.rect(surf, col, self.rect, border_radius=5)
        pygame.draw.rect(surf, C.TRACK, self.rect, 2, border_radius=5)
        txt = self.font.render(self.text, True, C.WHITE)
        surf.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))
