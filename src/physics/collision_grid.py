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

import math
from collections import defaultdict


class SpatialHashGrid:
    def __init__(self, cell_size: float, max_radius: float, max_displacement: float):
        self.cell_size = max(cell_size, 1e-6)
        self.max_radius = max_radius
        self.max_displacement = max_displacement
        self.cells = defaultdict(list)

    def _cell_of(self, x, y):
        return math.floor(x / self.cell_size), math.floor(y / self.cell_size)

    def insert(self, body):
        self.cells[self._cell_of(body.x, body.y)].append(body)

    def candidates_near(self, body, dt_sim: float = 0.0):
        ix, iy = self._cell_of(body.x, body.y)
        displacement = math.hypot(body.vx, body.vy) * abs(dt_sim)
        search_radius = (
            displacement
            + self.max_displacement
            + body.radius
            + self.max_radius
        )
        cell_range = max(1, math.ceil(search_radius / self.cell_size))
        result = []
        for dx in range(-cell_range, cell_range + 1):
            for dy in range(-cell_range, cell_range + 1):
                result.extend(self.cells.get((ix + dx, iy + dy), ()))
        return result


def build_collision_grid(circles, dt_sim: float = 0.0):
    if not circles:
        return None
    max_radius = max(c.radius for c in circles)
    max_displacement = max(
        math.hypot(c.vx, c.vy) * abs(dt_sim)
        for c in circles
    )
    grid = SpatialHashGrid(
        cell_size=max(2 * max_radius, 1.0),
        max_radius=max_radius,
        max_displacement=max_displacement,
    )
    for c in circles:
        grid.insert(c)
    return grid
    