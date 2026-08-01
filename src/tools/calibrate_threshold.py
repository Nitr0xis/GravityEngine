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

import time
import random
from physics.quadtree import build_quadtree
from physics.forces_manager import compute_forces_vectorized

class FakeCircle:
    def __init__(self, x, y, mass, radius):
        self.x, self.y, self.mass, self.radius = x, y, mass, radius
        self.attract_forces = []

def make_bodies(n):
    return [FakeCircle(random.uniform(0, 1e9), random.uniform(0, 1e9),
                        random.uniform(1e20, 1e26), random.uniform(1e5, 1e7))
            for _ in range(n)]

G = 6.6743e-11
for n in [50, 100, 150, 200, 300, 400, 500, 550, 600, 650, 700, 1000, 1500]:
    bodies = make_bodies(n)

    t0 = time.perf_counter()
    tree = build_quadtree(bodies)
    for b in bodies:
        tree.compute_force(b, 0.5, G, False)
    t_bh = time.perf_counter() - t0

    t0 = time.perf_counter()
    compute_forces_vectorized(bodies, G, False)
    t_np = time.perf_counter() - t0

    winner = "Barnes-Hut" if t_bh < t_np else "NumPy"
    print(f"n={n:5d} | BH: {t_bh*1000:6.2f}ms | NumPy: {t_np*1000:6.2f}ms | -> {winner}")
