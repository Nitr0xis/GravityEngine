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

from math import sqrt, atan2, cos, sin


class QuadNode:
    __slots__ = ("cx", "cy", "half", "mass", "com_x", "com_y",
                 "children", "bodies", "is_leaf")

    def __init__(self, cx, cy, half):
        self.cx, self.cy, self.half = cx, cy, half
        self.mass = 0.0
        self.com_x = 0.0
        self.com_y = 0.0
        self.children = None
        self.bodies = []       # list of bodies if this is a leaf (normally contains 1)
        self.is_leaf = True

    def _quadrant_index(self, x, y):
        idx = 0
        if x > self.cx:
            idx |= 1
        if y > self.cy:
            idx |= 2
        return idx

    def _child_bounds(self, idx):
        q = self.half / 2
        dx = q if idx & 1 else -q
        dy = q if idx & 2 else -q
        return self.cx + dx, self.cy + dy, q

    def _accumulate(self, body):
        total_mass = self.mass + body.mass
        self.com_x = (self.com_x * self.mass + body.x * body.mass) / total_mass
        self.com_y = (self.com_y * self.mass + body.y * body.mass) / total_mass
        self.mass = total_mass

    def insert(self, body):
        if self.children is not None:
            self._accumulate(body)
            self._insert_into_child(body)
            return

        if not self.bodies:
            self.bodies.append(body)
            self.mass = body.mass
            self.com_x, self.com_y = body.x, body.y
            return

        # Physical stopping criterion: if this node is already smaller than the
        # radii of the bodies it contains, subdividing further makes no geometric
        # sense (the bodies already fill the cell). We keep them together in a "dense" 
        # leaf, which is then treated exactly (pairwise) when computing forces — negligible 
        # cost because this only happens for nearly overlapping bodies.
        smallest_radius = min(b.radius for b in self.bodies + [body])
        if self.half <= max(smallest_radius, 1e-9):
            self._accumulate(body)
            self.bodies.append(body)
            return

        # Otherwise: normal subdivision
        old_bodies = self.bodies
        self.bodies = []
        self.children = [None, None, None, None]
        self.is_leaf = False
        for b in old_bodies:
            self._insert_into_child(b)

        self._accumulate(body)
        self._insert_into_child(body)

    def _insert_into_child(self, body):
        idx = self._quadrant_index(body.x, body.y)
        if self.children[idx] is None:
            cx, cy, half = self._child_bounds(idx)
            self.children[idx] = QuadNode(cx, cy, half)
        self.children[idx].insert(body)

    def compute_force(self, on_body, theta, G, reversed_gravity):
        if self.mass == 0.0:
            return 0.0, 0.0

        if self.children is None:
            # Leaf: do exact sum over the (rare) bodies it contains
            fx_total, fy_total = 0.0, 0.0
            for other in self.bodies:
                if other is on_body:
                    continue
                dx = other.x - on_body.x
                dy = other.y - on_body.y
                distance = sqrt(dx * dx + dy * dy)
                if distance <= on_body.radius + other.radius:
                    continue
                force = G * (on_body.mass * other.mass) / (distance ** 2)
                angle = atan2(dy, dx)
                fx, fy = cos(angle) * force, sin(angle) * force
                if reversed_gravity:
                    fx, fy = -fx, -fy
                fx_total += fx
                fy_total += fy
            return fx_total, fy_total

        dx = self.com_x - on_body.x
        dy = self.com_y - on_body.y
        distance = sqrt(dx * dx + dy * dy)
        if distance < 1e-9:
            distance = 1e-9

        if (self.half * 2 / distance) < theta:
            force = G * (on_body.mass * self.mass) / (distance ** 2)
            angle = atan2(dy, dx)
            fx, fy = cos(angle) * force, sin(angle) * force
            if reversed_gravity:
                fx, fy = -fx, -fy
            return fx, fy

        fx_total, fy_total = 0.0, 0.0
        for child in self.children:
            if child is not None:
                cfx, cfy = child.compute_force(on_body, theta, G, reversed_gravity)
                fx_total += cfx
                fy_total += cfy
        return fx_total, fy_total


def build_quadtree(circles):
    if not circles:
        return None
    xs = [c.x for c in circles]
    ys = [c.y for c in circles]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    half = max(max_x - min_x, max_y - min_y, 1.0) / 2 * 1.001
    root = QuadNode(cx, cy, half)
    for c in circles:
        root.insert(c)
    return root