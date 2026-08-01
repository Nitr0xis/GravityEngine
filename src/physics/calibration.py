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
Automatic calibration of the NumPy / Barnes-Hut threshold.

Executed once at startup (Engine.__init__). Tests increasing sizes
of n, stops as soon as Barnes-Hut wins twice — past this point,
the advantage is considered stable enough to not continue testing
(each test adds startup time overhead).
"""

import time
import random

from physics.quadtree import build_quadtree
from physics.forces_manager import compute_forces_vectorized


class _CalibrationBody:
    """Minimal object, duck-typed to satisfy build_quadtree / compute_forces_vectorized."""
    __slots__ = ("x", "y", "mass", "radius", "attract_forces")

    def __init__(self, x, y, mass, radius):
        self.x, self.y, self.mass, self.radius = x, y, mass, radius
        self.attract_forces = []


def _make_bodies(n):
    return [
        _CalibrationBody(
            random.uniform(0, 1e9), random.uniform(0, 1e9),
            random.uniform(1e20, 1e26), random.uniform(1e5, 1e7),
        )
        for _ in range(n)
    ]


def calibrate_force_threshold(
    G: float,
    candidate_ns=(200, 400, 600, 800, 1000, 1500, 2000, 3000, 5000, 8000),
    bh_theta: float = 0.5,
    bh_wins_to_stop: int = 2,
    default_threshold: int = 800,
) -> int:
    """
    Tests increasing n, NumPy vs Barnes-Hut, stops after
    `bh_wins_to_stop` wins by Barnes-Hut.

    Returns the n value at which Barnes-Hut has its first win (switching threshold),
    or `default_threshold` if Barnes-Hut never wins in the tested range.
    """
    bh_win_count = 0
    first_bh_win_n = None

    for n in candidate_ns:
        bodies = _make_bodies(n)

        t0 = time.perf_counter()
        tree = build_quadtree(bodies)
        for b in bodies:
            tree.compute_force(b, bh_theta, G, False)
        t_bh = time.perf_counter() - t0

        # Fresh arrays, to avoid any cache effect that could benefit either method
        bodies = _make_bodies(n)
        t0 = time.perf_counter()
        compute_forces_vectorized(bodies, G, False)
        t_np = time.perf_counter() - t0

        if t_bh < t_np:
            bh_win_count += 1
            if first_bh_win_n is None:
                first_bh_win_n = n
            if bh_win_count >= bh_wins_to_stop:
                return first_bh_win_n
        else:
            # A NumPy win after a BH win invalidates the trend
            # (noisy region): reset the win counter and forget
            # the first BH win, as it was not reliable.
            bh_win_count = 0
            first_bh_win_n = None

    return default_threshold
