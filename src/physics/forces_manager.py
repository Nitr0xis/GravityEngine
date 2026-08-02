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

import numpy as np
from physics.quadtree import build_quadtree


def compute_forces(circles, G, reversed_gravity, n_threshold, method_state,
                    hysteresis=100, barnes_hut_theta=0.5, force_barnes_hut=False):
    n = len(circles)
    if n == 0:
        return
    if n == 1:
        circles[0].attract_forces.clear()
        circles[0].attract_forces.append((0.0, 0.0))
        return

    if force_barnes_hut:
        use_bh = True
    elif method_state['last'] == 'numpy':
        use_bh = n > n_threshold + hysteresis
    else:
        use_bh = n > n_threshold - hysteresis

    method_state['last'] = 'barnes_hut' if use_bh else 'numpy'

    if use_bh:
        tree = build_quadtree(circles)
        for circle in circles:
            circle.attract_forces.clear()
            fx, fy = tree.compute_force(circle, barnes_hut_theta, G, reversed_gravity)
            circle.attract_forces.append((fx, fy))
    else:
        compute_forces_vectorized(circles, G, reversed_gravity)


def compute_forces_vectorized(circles, G, reversed_gravity):
    """
    Calculates gravitational forces for all bodies using O(n²) vectorized operations.
    Directly fills each circle's attract_forces list.
    """
    n = len(circles)
    if n == 0:
        return
    if n == 1:
        circles[0].attract_forces.clear()
        circles[0].attract_forces.append((0.0, 0.0))
        return

    x = np.array([c.x for c in circles])
    y = np.array([c.y for c in circles])
    mass = np.array([c.mass for c in circles])
    radius = np.array([c.radius for c in circles])

    dx = x[np.newaxis, :] - x[:, np.newaxis]
    dy = y[np.newaxis, :] - y[:, np.newaxis]
    dist2 = dx**2 + dy**2

    r_sum = radius[np.newaxis, :] + radius[:, np.newaxis]
    collision_mask = dist2 <= r_sum**2
    np.fill_diagonal(collision_mask, True)

    dist2_safe = np.where(collision_mask, np.inf, dist2)

    force_mag = G * (mass[:, np.newaxis] * mass[np.newaxis, :]) / dist2_safe
    angle = np.arctan2(dy, dx)
    fx = np.where(collision_mask, 0.0, np.cos(angle) * force_mag)
    fy = np.where(collision_mask, 0.0, np.sin(angle) * force_mag)

    if reversed_gravity:
        fx, fy = -fx, -fy

    fx_total = fx.sum(axis=1)
    fy_total = fy.sum(axis=1)

    for i, circle in enumerate(circles):
        circle.attract_forces.clear()
        circle.attract_forces.append((float(fx_total[i]), float(fy_total[i])))
        