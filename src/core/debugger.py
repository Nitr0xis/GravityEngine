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

import os
import sys
from core import state
from physics.circle import Circle


class Debugger:
    @staticmethod
    def default_debug():
        # DEBUG: Print paths for troubleshooting resource loading
        # This helps diagnose issues with font and asset loading in different environments
        print("=" * 60)
        print("RESOURCE PATH DEBUG")
        print("=" * 60)
        print(f"__file__: {os.path.abspath(__file__)}")
        print(f"Script dir: {os.path.dirname(os.path.abspath(__file__))}")
        print(f"Project root: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")

        # Check if running as PyInstaller bundle or in development mode
        if hasattr(sys, '_MEIPASS'):
            print(f"PyInstaller mode: {sys._MEIPASS}")
        else:
            print("Development mode")

        eng = state.engine
        if eng is None:
            print("engine: not initialized (default_debug called before Engine.__init__ completed)")
            print("=" * 60)
            return

        test_font = eng.fm.resource_path("assets/fonts/main_font.ttf")
        print(f"Font path: {test_font}")
        print(f"Font exists: {os.path.exists(test_font)}")
        print("=" * 60)

    @staticmethod
    def test_force_summation():
        """Check if the forces are properly summed, not averaged."""
        # Create a body
        body = Circle(x=500, y=500, density=5515, mass=1e20)
        
        # Simulate 3 identical forces
        body.attract_forces = [
            (10.0, 0.0),
            (10.0, 0.0),
            (10.0, 0.0)
        ]
        
        # Calculate the resulting force
        body.physics_update(1 / 120)
        
        # Verify that the force is 30, not 10
        assert body.force[0] == 30.0, f"Force should be 30, got {body.force[0]}"
        assert body.force[1] == 0.0
        print("Test force summation successful")
    
    @staticmethod
    def test_determinism():
        """
        Check if the simulation is determinist.
        Two same runs.
        """
        from core.main import Engine

        engine1 = Engine()
        engine2 = Engine()
        
        body1_a = Circle(x=500, y=500, density=5515, mass=1e24)
        body1_b = Circle(x=500, y=500, density=5515, mass=1e24)
        
        body2_a = Circle(x=700, y=500, density=5515, mass=1e24)
        body2_b = Circle(x=700, y=500, density=5515, mass=1e24)
        
        # simulate for 1000 steps
        for _ in range(1000):
            # Simulation A
            body1_a.attract_forces = [body1_a.attract(body2_a)]
            body2_a.attract_forces = [body2_a.attract(body1_a)]
            body1_a.physics_update(engine1.physics_timestep)
            body2_a.physics_update(engine1.physics_timestep)
            
            # Simulation B
            body1_b.attract_forces = [body1_b.attract(body2_b)]
            body2_b.attract_forces = [body2_b.attract(body1_b)]
            body1_b.physics_update(engine2.physics_timestep)
            body2_b.physics_update(engine2.physics_timestep)
        
        assert abs(body1_a.x - body1_b.x) < 1e-10, "X positions differ!"
        assert abs(body1_a.y - body1_b.y) < 1e-10, "Y positions differ!"
        
        print("Test determinism successful")

    @staticmethod
    def test_uniform_speed():
        """
        Check if it is always the same simulation speed.
        """
        # Simulation A : 120 FPS (2 frames)
        body_a = Circle(x=500, y=500, density=5515, mass=1e24)
        other_a = Circle(x=700, y=500, density=5515, mass=1e24)
        
        dt = 1.0 / 120  # 0.00833 s
        for _ in range(2):
            body_a.attract_forces = [body_a.attract(other_a)]
            body_a.physics_update(dt)
        
        # Simulation B : 60 FPS simulated (1 frame, but 2 physics steps)
        body_b = Circle(x=500, y=500, density=5515, mass=1e24)
        other_b = Circle(x=700, y=500, density=5515, mass=1e24)
        
        # 1 frame of 60 FPS = 16.67 ms = 2× physics timesteps
        for _ in range(2):  # 2 physics steps
            body_b.attract_forces = [body_b.attract(other_b)]
            body_b.physics_update(dt)
        
        assert abs(body_a.x - body_b.x) < 1e-10, "Different pos"
        
        print("Test uniform speed successful")

    @staticmethod
    def test_position_interpolation():
        """Test that position interpolation works correctly."""
        body = Circle(x=0, y=0, density=5515, mass=1e20)
        body.prev_x = 0.0
        body.prev_y = 0.0
        body.x = 100.0
        body.y = 100.0
        
        # Test alpha = 0.0 (should be at previous position)
        state = body.get_interpolated_state(0.0)
        assert abs(state['x'] - 0.0) < 1e-6, "Alpha=0 should give prev_x"
        assert abs(state['y'] - 0.0) < 1e-6, "Alpha=0 should give prev_y"
        
        # Test alpha = 1.0 (should be at current position)
        state = body.get_interpolated_state(1.0)
        assert abs(state['x'] - 100.0) < 1e-6, "Alpha=1 should give x"
        assert abs(state['y'] - 100.0) < 1e-6, "Alpha=1 should give y"
        
        # Test alpha = 0.5 (should be at midpoint)
        state = body.get_interpolated_state(0.5)
        assert abs(state['x'] - 50.0) < 1e-6, "Alpha=0.5 should give midpoint"
        assert abs(state['y'] - 50.0) < 1e-6, "Alpha=0.5 should give midpoint"
        
        print("Test position interpolation successful")

    @staticmethod
    def test_velocity_interpolation():
        """Test that velocity interpolation works correctly."""
        body = Circle(x=0, y=0, density=5515, mass=1e20)
        body.prev_vx = 0.0
        body.prev_vy = 0.0
        body.vx = 10.0
        body.vy = 10.0
        
        # Test alpha = 0.5
        state = body.get_interpolated_state(0.5)
        assert abs(state['vx'] - 5.0) < 1e-6, "Velocity should interpolate"
        assert abs(state['vy'] - 5.0) < 1e-6, "Velocity should interpolate"
        
        print("Test velocity interpolation successful")

    @staticmethod
    def test_force_interpolation():
        """Test that force interpolation works correctly."""
        body = Circle(x=0, y=0, density=5515, mass=1e20)
        body.prev_force = [0.0, 0.0]
        body.force = [1000.0, 1000.0]
        
        # Test alpha = 0.25
        state = body.get_interpolated_state(0.25)
        assert abs(state['fx'] - 250.0) < 1e-6, "Force should interpolate"
        assert abs(state['fy'] - 250.0) < 1e-6, "Force should interpolate"
        
        print("Test force interpolation successful")

    @staticmethod
    def test_interpolation_cache():
        """Test that interpolation cache works correctly."""
        body = Circle(x=0, y=0, density=5515, mass=1e20)
        body.x = 100.0
        body.prev_x = 0.0
        
        # First call should compute
        state1 = body.get_interpolated_state(0.5)
        
        # Second call with same alpha should use cache
        state2 = body.get_interpolated_state(0.5)
        
        # Should be same object (cache hit)
        assert state1 is state2, "Cache should return same object"
        
        # Different alpha should recompute
        state3 = body.get_interpolated_state(0.6)
        assert state1 is not state3, "Different alpha should recompute"
        
        print("Test interpolation cache successful")

    @staticmethod
    def test_barnes_hut_matches_brute_force():
        """theta=0 doit reproduire exactement la somme des forces brutes."""
        from physics.quadtree import build_quadtree

        bodies = [
            Circle(x=0, y=0, density=5515, mass=1e24),
            Circle(x=1e7, y=0, density=5515, mass=2e24),
            Circle(x=0, y=1e7, density=5515, mass=3e23),
        ]

        root = build_quadtree(bodies)
        for b in bodies:
            bh_fx, bh_fy = root.compute_force(b, 0.0, state.engine.gravity, False)
            brute_fx = brute_fy = 0.0
            for other in bodies:
                if other is not b:
                    fx, fy = b.attract(other)
                    brute_fx += fx
                    brute_fy += fy
            assert abs(bh_fx - brute_fx) < 1e-6
            assert abs(bh_fy - brute_fy) < 1e-6
        print("Test Barnes-Hut (theta=0) == brute force successful")

    @staticmethod
    def test_vectorized_matches_brute_force():
        from physics.forces_manager import compute_forces_vectorized

        bodies = [
            Circle(x=0, y=0, density=5515, mass=1e24),
            Circle(x=1e7, y=0, density=5515, mass=2e24),
            Circle(x=0, y=1e7, density=5515, mass=3e23),
        ]

        compute_forces_vectorized(bodies, state.engine.gravity, False)
        vec_forces = [tuple(b.attract_forces[0]) for b in bodies]

        for i, b in enumerate(bodies):
            brute_fx = brute_fy = 0.0
            for other in bodies:
                if other is not b:
                    fx, fy = b.attract(other)
                    brute_fx += fx
                    brute_fy += fy
            assert abs(vec_forces[i][0] - brute_fx) < 1e-6
            assert abs(vec_forces[i][1] - brute_fy) < 1e-6

        print("Test vectorized forces == brute force successful")
