"""
Gravity Engine 3.4.0 by Nitr0xis (Nils DONTOT) - Real-time N-body Gravity Simulator
Copyright (c) 2026 Nils DONTOT

--- Informations ---
Email: nils.dontot.pro@gmail.com
GitHub account: https://github.com/Nitr0xis/
GitHub repository: https://github.com/Nitr0xis/GravityEngine/
LICENCE: https://creativecommons.org/licenses/by-nc-sa/4.0/, Creative Commons BY-NC-SA 4.0 License
README: https://github.com/Nitr0xis/GravityEngine/blob/main/README.md

--- Dependencies ---
Pygame: https://www.pygame.org/
Atlas - My own file managing module:
    Email: nils.dontot.pro@gmail.com
    GitHub account: https://github.com/Nitr0xis/
    GitHub repository: https://github.com/Nitr0xis/Atlas/
    LICENCE: https://creativecommons.org/licenses/by-nc-sa/4.0/, Creative Commons BY-NC-SA 4.0 License
    README: https://github.com/Nitr0xis/Atlas/blob/main/README.md

CONTROLS:
    H/I : Display info
    A/E : Zoom in/Zoom out
    Space : Pause/Unpause      
    V : Toggle vectors    
    R : Random mode
    G : Toggle reversed gravity     
    P : Generate 20 bodies
    T : Reset camera zoom
    Delete : Delete selected     
    Escape : Exit
    Left click : Click to select/create bodies, hold to increase size
    Right click : Move the camera
    Mouse wheel (optional) : Zoom in and Zoom out

CONFIGURATION (in Engine.__init__()) (Main parameters):
    performance_mode      : "precise" (accurate) or "adaptive" (fast)
    time_acceleration     : Simulation speed (default: 4e6)
    min_physics_interval  : Update rate in adaptive mode (default: 0.025s)
    FPS_TARGET            : Rendering FPS (default: 120)
    default_density       : Body density kg/m³ (default: 5514)
    fusions               : Enable/disable body fusion (default: True)

MODES:
    PRECISE (default) : Fixed timestep, deterministic, may slow with many bodies
    ADAPTIVE : Throttled updates, smooth rendering, less accurate

PHYSICS:
    Newtonian gravity (F = G×m₁×m₂/r²), momentum conservation,
    fixed/adaptive timestep, visual collision detection
"""


# Standard library imports
import importlib.util  # For dynamic module checking
import os  # For file system operations
import subprocess  # For installing missing modules
import random  # For random number generation
import time  # For time tracking and delays
import sys  # For system-specific parameters and functions
from tkinter import NO
from typing import Optional  # For args typing
import warnings  # Used to display warning messages about deprecated features or potential issues

# Import all math functions for convenience (sqrt, sin, cos, atan2, etc.)
from math import *


# Required external modules for the simulation
REQUIRED_MODULES: set[str] = {"pygame"}

# Automatically install missing required modules
for module in REQUIRED_MODULES:
    if importlib.util.find_spec(module) is None:
        # Install module using pip if not found
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        except subprocess.CalledProcessError:
            warnings.warn(f"The pre-installation of the module {module} has failed.")

# Import pygame after ensuring it's installed
try:
    import pygame
except ImportError:
    raise ImportError("\"pygame\" module is not installed")

# Import my own modules
from atlas import FileManager


"""
Todo:
    - Use my own module for file managing
    - Add screenshots
    - add the holding of camera keys
    - add a focus mode
    - add a "define as referential button"
    - add collision epsilon
    - add a color field which shows the attract field of the selected body
    - consider quadtree system for forces
    - mass transfer on collision without fusion
    - add senarios in json
    - add .csv export method

For my NSI projects:
    - add a dynamic configure pannel (choice between pygame and tkinter)
    - advanced data system with curves (choice between pygame and tkinter) [using matplotlib + tkinter in the same window]

Ideas:
    -=-=-=-=-
"""


# ==================================================================================
# ==================================================================================


# -----------------
# class Color
# -----------------
class Color:
    def __init__(self, *values):
        if len(values) not in (3, 4):
            raise ValueError("Color must have 3 (RGB) or 4 (RGBA) values")
        
        if not all(isinstance(v, int) and 0 <= v <= 255 for v in values):
            raise ValueError("All values must be integers between 0 and 255")
        
        self._value = tuple[int, ...](values)
    
    @property
    def value(self):
        return self._value
    
    @property
    def rgb(self):
        return self._value[:3]
    
    @property
    def alpha(self):
        return self._value[3] if len(self._value) == 4 else 255
    
    @property
    def average(self):
        """Returns the mean of the RGB components (average brightness)"""
        return sum(self.rgb) / 3
    
    @property
    def luminosity(self):
        """Perceived luminosity (standard formula for comparisons)"""
        r, g, b = self.rgb
        return 0.299 * r + 0.587 * g + 0.114 * b
    
    def __iter__(self):
        """Allows: tuple(color), list(color), *color"""
        return iter(self._value)

    def __getitem__(self, index):
        """Allows: color[0], color[1], color[2]"""
        return self._value[index]

    def __len__(self):
        """Allows: len(color)"""
        return len(self._value)
    
    # ADDITION: color1 + color2
    def __add__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only add another Color")
        
        max_len = max(len(self._value), len(other._value))
        v1 = self._value + (255,) * (max_len - len(self._value))
        v2 = other._value + (255,) * (max_len - len(other._value))
        
        result = tuple(min(255, a + b) for a, b in zip(v1, v2))
        return Color(*result)
    
    # SUBTRACTION: color1 - color2
    def __sub__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only subtract another Color")
        
        max_len = max(len(self._value), len(other._value))
        v1 = self._value + (255,) * (max_len - len(self._value))
        v2 = other._value + (255,) * (max_len - len(other._value))
        
        result = tuple(max(0, a - b) for a, b in zip(v1, v2))
        return Color(*result)
    
    # MULTIPLICATION: color * 2 or color * 0.5
    def __mul__(self, factor):
        if not isinstance(factor, (int, float)):
            raise TypeError("Can only multiply by a number")
        
        result = tuple(int(min(255, max(0, v * factor))) for v in self._value)
        return Color(*result)
    
    def __rmul__(self, factor):
        return self.__mul__(factor)
    
    # DIVISION: color / 2
    def __truediv__(self, factor):
        if not isinstance(factor, (int, float)):
            raise TypeError("Can only divide by a number")
        if factor == 0:
            raise ValueError("Division by zero")
        
        result = tuple(int(min(255, max(0, v / factor))) for v in self._value)
        return Color(*result)
    
    # AVERAGE: color1 // color2
    def __floordiv__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only average with another Color")
        
        max_len = max(len(self._value), len(other._value))
        v1 = self._value + (255,) * (max_len - len(self._value))
        v2 = other._value + (255,) * (max_len - len(other._value))
        
        result = tuple((a + b) // 2 for a, b in zip(v1, v2))
        return Color(*result)
    
    # EQUALITY: color1 == color2
    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return self._value == other._value
    
    # DIFFERENCE: color1 != color2
    def __ne__(self, other):
        return not self.__eq__(other)
    
    # COMPARISONS (based on perceived luminosity)
    def __lt__(self, other):
        """color1 < color2: compares luminosity"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity < other.luminosity
    
    def __le__(self, other):
        """color1 <= color2"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity <= other.luminosity
    
    def __gt__(self, other):
        """color1 > color2"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity > other.luminosity
    
    def __ge__(self, other):
        """color1 >= color2"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity >= other.luminosity
    
    def __repr__(self):
        return f"Color{self._value}"
    
    def __str__(self):
        r, g, b = self.rgb
        if len(self._value) == 4:
            return f"Color(R:{r}, G:{g}, B:{b}, A:{self.alpha})"
        return f"Color(R:{r}, G:{g}, B:{b})"


# -----------------
# class Display
# -----------------
class Display:
    # Color constants (RGB tuples)
    # These define the color palette used throughout the simulation
    WHITE = Color(255, 255, 255)  # Default body color in dark mode
    BLUE = Color(10, 124, 235)  # UI text and information color
    SP_BLUE = Color(130, 130, 220)  # Special blue for force vectors
    BLACK = Color(0, 0, 0)  # Background in dark mode, default body color in light mode
    DUCKY_GREEN = Color(28, 201, 89)  # Selection highlight color
    GREEN = Color(0, 255, 0)  # X-component velocity vector color
    YELLOW = Color(241, 247, 0)  # Y-component velocity vector color
    DARK_GREY = Color(100, 100, 100)  # Body shadow/outline color
    RED = Color(255, 0, 0)  # Global velocity vector color


# -----------------
# class Tester
# -----------------
class Tester:
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

        # Test font path resolution
        test_font = engine.fm.resource_path('assets/font.ttf')
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
        body.update()
        
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
        
        print("✓ Test determinism successful")

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
        
        print("✓ Test uniform speed successful")

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
        
        print("✓ Test position interpolation successful")

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
        
        print("✓ Test velocity interpolation successful")

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
        
        print("✓ Test force interpolation successful")

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
        
        print("✓ Test interpolation cache successful")


# -----------------
# class TempText
# -----------------
class TempText:
    """
    Temporary text display class for showing messages on screen.
    
    Automatically manages its own lifecycle - removes itself from the display
    list when the duration expires. Used for notifications and status messages.
    """
    def __init__(self, text: str = "", duration: float = 1, dest: tuple[float, float] = (0, 0), line: int = 0,
                 color: tuple[int, int, int] | tuple[int, int, int, int] = (10, 124, 235)):
        """
        Initialize a temporary text object.
        
        Args:
            text: The text string to display
            duration: How long the text should remain visible (in seconds)
            dest: Initial position (x, y) on screen
            line: Line offset for vertical spacing (0 = first line)
            color: RGB or RGBA color tuple for the text
        """
        super().__init__()

        # Register this text in the engine's temporary texts list
        engine.temp_texts.append(self)

        # Record creation time for expiration checking
        self.birth_time = time.time()

        # Store text properties
        self.text = text
        self.duration = duration

        # Calculate position with line offset
        self.x = dest[0]
        self.y = dest[1] + line * (engine.txt_gap + engine.txt_size)
        self.line = line
        self.color = color

        # Rectangle for collision/position tracking (not currently used)
        self.rect = None

    def update(self):
        """
        Update the temporary text - draw it if still valid, remove if expired.
        
        Returns:
            True if text is still active, False if expired and removed
        """
        # Check if duration has expired
        if time.time() - self.birth_time > self.duration:
            # Remove from list if still present
            if self in engine.temp_texts:
                engine.temp_texts.remove(self)
            return False
        else:
            # Draw the text at its position
            Utils.write_screen(self.text, (self.x, self.y + self.line * (engine.txt_gap + engine.txt_size)),
                        self.color)
            return True


# -----------------
# class Camera
# -----------------
class Camera:
    def __init__(self, x: float = 0.0, y: float = 0.0, scale: float = 1.0, scale_step: float = 1.1):
        # ===== CAMERA POSITION =====
        self.cam_x = x  # Camera X offset (in screen pixels)
        self.cam_y = y  # Camera Y offset (in screen pixels)
        
        # ===== ZOOM =====
        self.scale = scale  # Zoom factor (1.0 = normal, 2.0 = 2x zoom)
        self.scale_step = scale_step  # Zoom multiplier (1.1 = +10% per step)
        
        # ===== LIMITS =====
        self.min_scale = 0.001  # Minimum zoom (very zoomed out)
        self.max_scale = 100.0  # Maximum zoom (very zoomed in)
        
        # ===== PANNING =====
        self.pan_speed = 5.0  # Panning speed (pixels per frame)
        self.is_panning = False  # Whether we are currently panning the view
        self.pan_start_x = 0  # Pan start position X
        self.pan_start_y = 0

    def zoom_at_mouse(self, zoom_in: bool):
        """
        Zoom centered on the mouse position.
        
        Args:
            zoom_in: True to zoom in, False to zoom out
        """
        mx, my = pygame.mouse.get_pos()

        # World position BEFORE zoom
        wx, wy = self.screen_to_world(mx, my)

        # Apply zoom
        if zoom_in:
            self.scale *= self.scale_step
        else:
            self.scale /= self.scale_step

        # Clamp to allowed range
        self.scale = max(self.min_scale, min(self.scale, self.max_scale))

        # Recalculate offset to keep (wx, wy) under the mouse
        self.cam_x = mx - wx * self.scale
        self.cam_y = my - wy * self.scale
    
    def screen_to_world(self, sx, sy):
        """
        Convert screen coordinates → world coordinates.
        
        Args:
            sx, sy: Screen coordinates (pixels)
        
        Returns:
            wx, wy: World coordinates (meters)
        """
        wx = (sx - self.cam_x) / self.scale
        wy = (sy - self.cam_y) / self.scale
        return wx, wy

    def world_to_screen(self, wx, wy):
        """
        Convert world coordinates → screen coordinates.
        
        Args:
            wx, wy: World coordinates (meters)
        
        Returns:
            sx, sy: Screen coordinates (pixels)
        """
        sx = wx * self.scale + self.cam_x
        sy = wy * self.scale + self.cam_y
        return sx, sy
    
    def start_pan(self, mouse_x, mouse_y):
        """Start panning the view."""
        self.is_panning = True
        self.pan_start_x = mouse_x
        self.pan_start_y = mouse_y
    
    def update_pan(self, mouse_x, mouse_y):
        """Update the panning of the view."""
        if self.is_panning:
            # Calculate the mouse movement
            dx = mouse_x - self.pan_start_x
            dy = mouse_y - self.pan_start_y
            
            # Move the camera
            self.cam_x += dx
            self.cam_y += dy
            
            # Update the starting position
            self.pan_start_x = mouse_x
            self.pan_start_y = mouse_y
    
    def end_pan(self):
        """End view panning."""
        self.is_panning = False
    
    def reset(self):
        """Reset the camera to the default position."""
        self.cam_x = 0
        self.cam_y = 0
        self.scale = 1.0


# -----------------
# class Circle
# -----------------
class Circle:
    """
    Represents a celestial body in the gravity simulation.
    
    Each Circle object has physical properties (mass, radius, position, velocity)
    and can interact with other bodies through gravitational forces.
    """
    def __init__(self, x, y, density, mass):
        """
        Initialize a new celestial body.
        
        Args:
            x: Initial x-coordinate position
            y: Initial y-coordinate position
            density: Density of the body (mass per unit volume)
            mass: Mass of the body (determines size and gravitational influence)
        """
        super().__init__()

        # Position tracking
        self.pos = None  # Tuple (x, y) for position
        self.full_selected_mode = False  # Selection display mode flag

        # Assign unique identifier
        engine.circle_number += 1
        self.number: int = engine.circle_number

        # Position coordinates (converted to float for precision)
        self.x = float(x)
        self.y = float(y)

        # Mass properties
        self.basic_mass = mass  # Original mass (before fusion)
        self.mass = self.basic_mass  # Current mass (may change after fusion)

        # Density property (mass per unit volume, kg/m^3)
        self.density = float(density)

        # Radius calculation from mass and density
        # Volume = mass / density
        # Volume = (4/3) * π * r³
        # Therefore: r = ((3 * mass) / (4 * π * density))^(1/3)
        if self.density > 0:
            volume = self.mass / self.density
            self.radius = cbrt((3 * volume) / (4 * pi))
        else:
            # Fallback to default calculation if density is invalid
            self.radius = cbrt(self.mass)

        # Geometric properties
        self.surface = 4 * self.radius ** 2 * pi  # Surface area of sphere
        self.volume = 4 / 3 * pi * self.radius ** 3  # Volume of sphere

        # Rendering properties
        self.rect = None  # Pygame rectangle for collision detection

        # Color based on screen mode
        if engine.screen_mode == "dark":
            self.color = Display.WHITE
        elif engine.screen_mode == "light":
            self.color = Display.BLACK

        # Selection state
        self.is_selected = False
        if not self in circles:
            self.is_selected = False

        # Velocity components (meters per second)
        self.vx = 0.0  # Horizontal velocity, m/s
        self.vy = 0.0  # Vertical velocity, m/s

        self.ax = 0.0  # Horizontal acceleration, m/s²
        self.ay = 0.0  # Vertical acceleration, m/s²

        # Speed magnitude (total velocity)
        self.speed = sqrt(self.vx ** 2 + self.vy ** 2)  # m/s

        # Lifecycle flags
        self.suicide: bool = False  # Flag for removal after fusion

        # Previous positions for interpolation (rendering with time accumulator)
        # These store the position from the previous physics step
        # Used in draw_interpolated() to smooth rendering between physics updates
        # ==================== INTERPOLATION STATE ====================
        # Previous position
        self.prev_x = float(x)
        self.prev_y = float(y)
        
        # Previous velocities
        self.prev_vx = 0.0
        self.prev_vy = 0.0
        
        # Previous forces
        self.prev_force = [0.0, 0.0]
        
        # Previous radius
        self.prev_radius = self.radius

        # Cache for interpolated values (for recalculation avoidance)
        self._interpolated_cache = {
            'x': self.x,
            'y': self.y,
            'vx': 0.0,
            'vy': 0.0,
            'fx': 0.0,
            'fy': 0.0,
            'radius': self.radius,
            'alpha': -1.0  # -1 = invalid
        }

        # Age tracking
        self.is_born = False  # Whether body has been initialized in simulation
        self.birth_time = None  # Timestamp when body was created
        self.age = 0  # Age in simulation time
        self.simulation_time_in_pause = 0  # Time spent in paused state

        # UI positioning
        self.info_y: int = 6 * engine.txt_gap + 4 * engine.txt_size  # Y position for info display

        # Vector visualization properties
        self.vector_width = 1  # Line width for velocity vectors
        self.global_speed_vector_scale = 1e4  # in px/m/s
        self.force_vector_scale = 1e2  # in px/N

        # Vector colors
        self.GSV_color = Display.RED  # Global Speed Vector (total velocity)
        self.CSV_x_color = Display.GREEN  # Cardinal Speed Vector X component
        self.CSV_y_color = Display.YELLOW  # Cardinal Speed Vector Y component

        # Force tracking
        self.attract_forces: list[tuple[float, float]] = []  # List of force vectors from other bodies
        self.force: list[float] = [0.0, 0.0]  # Net force vector (x, y), in pixel variants
        self.printed_force: list[float] = [0.0, 0.0]  # Force for display (scaled to real units [Newtons])

    def kinetic_energy(self):
        """
        Calculate kinetic energy of the body.
        
        Formula: E = 0.5 * m * v²
        
        Returns:
            Kinetic energy in joules
        """
        return 0.5 * self.mass * (self.speed ** 2)

    def switch_selection(self):
        """Toggle selection state of the body."""
        self.is_selected = not self.is_selected

    def get_nearest(self) -> Optional[tuple[int, float]]:
        """
        Find the nearest body to this one.
        
        Calculates distance to all other bodies and returns the closest one.
        
        Returns:
            Tuple of (nearest_body_id, distance) or None if no other bodies exist
        """
        numbers = []
        distances = []

        # Calculate distance to all other bodies
        for other in circles:
            if other is not self:
                numbers.append(other.number)
                # Euclidean distance: sqrt((x2-x1)² + (y2-y1)²)
                distances.append(sqrt((self.y - other.y) ** 2 + (self.x - other.x) ** 2))

        # Return nearest body info if any exist
        if len(distances) != 0:
            min_distance = min(distances)
            nearest_index = distances.index(min_distance)
            return numbers[nearest_index], min_distance
        else:
            return None

    def print_global_speed_vector(self, in_terminal: bool = False, alpha: float = 1.0):
        """
        Print Global Speed Vector (total velocity vector) with camera transformation.
        
        Draws a line from the body's center showing the direction and magnitude
        of its total velocity. The length is scaled by velocity and time factor.

        Uses interpolated position AND velocity for smooth vector rendering.
        
        Args:
            in_terminal: If True, also print vector info to console
            alpha: Interpolation factor for smooth rendering (0 to 1)
        """
        # ===== GET INTERPOLATED STATE =====
        state = self.get_interpolated_state(alpha)
        
        world_x = state['x']
        world_y = state['y']
        render_vx = state['vx']  # <- Interpolated Speed
        render_vy = state['vy']  # <- Interpolated Speed
        
        # ===== CONVERT TO SCREEN COORDINATES =====
        screen_x1, screen_y1 = engine.camera.world_to_screen(world_x, world_y)
        
        # Calculer la position de fin du vecteur dans le monde
        world_x2 = world_x + render_vx * self.global_speed_vector_scale
        world_y2 = world_y + render_vy * self.global_speed_vector_scale

        # Convert to screen coordinates
        screen_x2, screen_y2 = engine.camera.world_to_screen(world_x2, world_y2)

        if in_terminal:
            speed_magnitude = sqrt(render_vx ** 2 + render_vy ** 2)
            print(f"N{self.number} Vector at alpha={alpha:.3f}:")
            print(f"  World position: ({world_x:.1f}, {world_y:.1f})")
            print(f"  Screen position: ({screen_x1:.1f}, {screen_y1:.1f})")
            print(f"  Velocity: ({render_vx:.2f}, {render_vy:.2f}) m/s")

        # ===== DRAW VELOCITY VECTOR =====
        Utils.draw_line(self.GSV_color, (screen_x1, screen_y1), (screen_x2, screen_y2), self.vector_width)

        if engine.cardinal_vectors:
            self.print_cardinal_speed_vectors(in_terminal, alpha)

    def print_force_vector(self, in_terminal: bool = False, alpha: float = 1.0):
        """
        Print the force vector (net gravitational force).
        
        Draws a line showing the direction and magnitude of the net force
        acting on the body from all other bodies.

        Uses interpolated position AND force for smooth vector rendering.
        Works with camera transformation.
        
        Args:
            in_terminal: If True, also print vector info to console
            alpha: Interpolation factor for smooth rendering (0 to 1)
        """
        # ===== GET INTERPOLATED STATE =====
        state = self.get_interpolated_state(alpha)
        
        world_x = state['x']
        world_y = state['y']
        render_fx = state['fx']  # <- Interpolated Force
        render_fy = state['fy']  # <- Interpolated Force

        # ===== CALCULATE FORCE MAGNITUDE =====
        force_magnitude = sqrt(self.force[0] ** 2 + self.force[1] ** 2)
        
        # Early exit if no force
        if force_magnitude < 1e-10:
            return
        
        # ===== CALCULATE UNIT VECTOR (DIRECTION) =====
        unit_x = render_fx / force_magnitude
        unit_y = render_fy / force_magnitude
        
        # ===== SCALE VECTOR FOR VISIBILITY =====
        # Use logarithmic scaling for very large/small forces
        # This compresses the range while preserving direction
        
        # Logarithmic scaling: log10(force) gives better visibility
        # Add 1 to avoid log(0), multiply by scale factors
        visual_length = log10(force_magnitude + 1) * engine.vector_scale * self.force_vector_scale
        
        # ===== CALCULATE END POINT IN WORLD COORDINATES =====
        vector_x = unit_x * visual_length
        vector_y = unit_y * visual_length
        world_end_x = world_x + vector_x
        world_end_y = world_y + vector_y
        
        # ===== CONVERT TO SCREEN COORDINATES =====
        screen_x1, screen_y1 = engine.camera.world_to_screen(world_x, world_y)
        screen_x2, screen_y2 = engine.camera.world_to_screen(world_end_x, world_end_y)

        if in_terminal:
            angle_deg = atan2(render_fy, render_fx) * 180 / pi
            print(f"N{self.number} Force at alpha={alpha:.3f}:")
            print(f"  World position: ({world_x:.1f}, {world_y:.1f})")
            print(f"  Screen position: ({screen_x1:.1f}, {screen_y1:.1f})")
            print(f"  Force: ({render_fx:.2e}, {render_fy:.2e}) N")
            print(f"  Magnitude: {force_magnitude:.2e} N")
            print(f"  Angle: {angle_deg:.1f}°")
            print(f"  Visual length: {visual_length:.1f} px")
        
        # ===== DRAW FORCE VECTOR =====
        Utils.draw_line(Display.SP_BLUE, (screen_x1, screen_y1), (screen_x2, screen_y2))

    def print_cardinal_speed_vectors(self, in_terminal: bool = False, alpha: float = 1.0):
        """
        Print Cardinal Speed Vectors (X and Y components separately).
        
        Draws two lines showing horizontal (X) and vertical (Y) velocity
        components independently. X component in green, Y component in yellow.

        Uses interpolated position and velocity.
        Works with camera transformation.
        
        Args:
            in_terminal: If True, also print vector info to console
            alpha: Interpolation factor for smooth rendering (0 to 1)
        """
        # ===== GET INTERPOLATED STATE =====
        state = self.get_interpolated_state(alpha)
        
        world_x = state['x']
        world_y = state['y']
        render_vx = state['vx']  # <- Interpolated X Speed
        render_vy = state['vy']  # <- Interpolated Y Speed

        # ===== CALCULATE VECTOR ENDPOINTS IN WORLD COORDINATES =====
        # X component (horizontal)
        world_x1 = world_x
        world_x2 = world_x + render_vx * self.global_speed_vector_scale
        
        # Y component (vertical)
        world_y1 = world_y
        world_y2 = world_y + render_vy * self.global_speed_vector_scale
        
        # ===== CONVERT TO SCREEN COORDINATES =====
        # For X component (horizontal line)
        screen_x1, screen_y1 = engine.camera.world_to_screen(world_x1, world_y)
        screen_x2, screen_y2 = engine.camera.world_to_screen(world_x2, world_y)
        
        # For Y component (vertical line)
        screen_x3, screen_y3 = engine.camera.world_to_screen(world_x, world_y1)
        screen_x4, screen_y4 = engine.camera.world_to_screen(world_x, world_y2)

        if in_terminal:
            print(f"N{self.number} Cardinal vectors at alpha={alpha:.3f}:")
            print(f"  World position: ({world_x:.1f}, {world_y:.1f})")
            print(f"  Screen position: ({screen_x1:.1f}, {screen_y1:.1f})")
            print(f"  Vx: {render_vx:.2f} m/s")
            print(f"  Vy: {render_vy:.2f} m/s")

        # ===== DRAW X COMPONENT (GREEN HORIZONTAL LINE) =====
        Utils.draw_line(self.CSV_x_color, (screen_x1, screen_y1), (screen_x2, screen_y2), self.vector_width)
        
        # ===== DRAW Y COMPONENT (YELLOW VERTICAL LINE) =====
        Utils.draw_line(self.CSV_y_color, (screen_x3, screen_y3), (screen_x4, screen_y4), self.vector_width)

    def print_info(self, y: int):
        """
        Display detailed information panel for the selected body.
        
        Shows physical properties, position, velocity, forces, and relationships
        to other bodies. Information is displayed in a formatted panel.
        
        Args:
            y: Y-coordinate for the info panel top position
        """
        # Draw separator line
        pygame.draw.rect(engine.screen, Display.BLUE, (20, y, 340, 5))

        # Body ID
        text = f"ID : {self.number}"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 1)

        # Age display (converted from simulation time to years)
        # 31,557,600 = seconds in a year
        age_years = self.age * engine.time_acceleration / 31_557_600
        if age_years < 2:
            text = f"Age : {round(age_years * 1000) / 1000} Earth year"
            Utils.write_screen(text, (20, y - 20), Display.BLUE, 2)
        else:
            text = f"Age : {round(age_years * 1000) / 1000} Earth years"
            Utils.write_screen(text, (20, y - 20), Display.BLUE, 2)

        # Mass (in kilograms)
        text = f"Mass : {self.mass:.2e} kg"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 3)

        # Radius (in meters)
        text = f"Radius : {round(self.radius * 10) / 10} m"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 4)

        # Volume (in cubic meters)
        text = f"Volume : {self.volume:.2e} m³"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 5)

        # Density (in kilograms by cubic meters)
        text = f"Density : {self.density:.2e} kg/m³"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 6)

        # Kinetic energy (in joules)
        text = f"Kinetic energy : {self.kinetic_energy():.2e} J"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 8)

        # Net force magnitude (in newtons)
        force_magnitude = sqrt(self.printed_force[0] ** 2 + self.printed_force[1] ** 2)
        text = f"Force applied : {force_magnitude:.2e} N"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 9)

        # Velocity magnitude (in m/s)
        text = f"Velocity : {self.speed:.2e} m/s"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 10)

        # Position coordinates
        text = f"Coordinates : {int(self.x)}; {int(self.y)}"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 11)

        # Nearest body information
        nearest_tuple = self.get_nearest()
        if nearest_tuple is not None:
            text = f"Nearest body : n°{nearest_tuple[0]} -> {round(nearest_tuple[1]):.2e} m"
            Utils.write_screen(text, (20, y - 20), Display.BLUE, 12)
        else:
            text = f"Nearest body : None"
            Utils.write_screen(text, (20, y - 20), Display.BLUE, 12)

    def reset_force_list(self):
        """Clear the list of gravitational forces from other bodies."""
        self.attract_forces = []

    def get_interpolated_state(self, alpha):
        """
        Calculate interpolated state for smooth rendering.
        
        Uses linear interpolation (PRECISE mode) for all properties.
        Results are cached to avoid recalculation within the same frame.
        
        Args:
            alpha: Interpolation factor (0.0 to 1.0)
                0.0 = exactly at previous physics state
                1.0 = exactly at current physics state
        
        Returns:
            dict: Interpolated state with keys:
                'x', 'y', 'vx', 'vy', 'fx', 'fy'
        """
        # Check cache validity
        if abs(self._interpolated_cache['alpha'] - alpha) < 1e-6:
            # Cache is valid for this alpha, return it
            return self._interpolated_cache
        
        # Calculate interpolated state (linear interpolation)
        state = {
            # Position interpolation
            'x': self.prev_x + (self.x - self.prev_x) * alpha,
            'y': self.prev_y + (self.y - self.prev_y) * alpha,
            
            # Velocity interpolation
            'vx': self.prev_vx + (self.vx - self.prev_vx) * alpha,
            'vy': self.prev_vy + (self.vy - self.prev_vy) * alpha,
            
            # Force interpolation
            'fx': self.prev_force[0] + (self.force[0] - self.prev_force[0]) * alpha,
            'fy': self.prev_force[1] + (self.force[1] - self.prev_force[1]) * alpha,
            
            # Radius interpolation
            'radius': self.prev_radius + (self.radius - self.prev_radius) * alpha,

            # Store alpha for cache validation
            'alpha': alpha
        }
        
        # Update cache
        self._interpolated_cache = state
        
        return state

    def attract(self, other, effective: bool = True) -> tuple[float, float]:
        """
        Calculate gravitational attraction force with another body.
        
        Uses Newton's law of universal gravitation:
        F = G * (m1 * m2) / r²
        
        Args:
            other: The other Circle object to calculate attraction with
            effective: If True, apply the force to velocity. If False, only return force vector.
        
        Returns:
            Tuple (fx, fy) representing force components in x and y directions
        """
        # Calculate distance components
        dx = other.x - float(self.x)
        dy = other.y - float(self.y)

        # Calculate Euclidean distance
        distance = float(sqrt((dx ** 2) + (dy ** 2)))

        # Skip force calculation if bodies are overlapping (collision)
        if distance <= self.radius + other.radius:
            return 0, 0

        # Calculate gravitational force magnitude
        # F = G * (m1 * m2) / r²
        force = engine.gravity * ((self.mass * other.mass) / (distance ** 2))
        
        # Calculate angle from self to other
        angle = atan2(dy, dx)

        # Decompose force into x and y components
        fx = cos(angle) * force
        fy = sin(angle) * force

        # Apply reversed gravity if enabled (repulsion instead of attraction)
        if engine.reversed_gravity:
            fx *= -1
            fy *= -1

        return fx, fy

    def physics_update(self, dt):
        """
        Physics update with fixed timestep.
        
        CRITICAL: Save previous state BEFORE any modifications
        for interpolation in rendering.
        
        Args:
            dt: Fixed physics timestep (always engine.physics_timestep)
        """
        # ===== SAVE PREVIOUS STATE FOR INTERPOLATION =====
        # This MUST be done BEFORE any state changes
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_vx = self.vx
        self.prev_vy = self.vy
        self.prev_force = self.force.copy()  # .copy() important!
        self.prev_radius = self.radius
        
        # Invalidate interpolation cache
        self._interpolated_cache['alpha'] = -1.0
        
        # ===== CALCULATE NET FORCE =====
        # Calculate net force from all gravitational interactions
        self.force = [0.0, 0.0]
        for f in self.attract_forces:
            self.force[0] += f[0]
            self.force[1] += f[1]
        
        # ===== UPDATE PHYSICS =====
        self.ax = self.force[0] / self.mass  # m/s²
        self.ay = self.force[1] / self.mass

        dt_sim = dt * engine.time_acceleration
        self.vx += self.ax * dt_sim  # m/s += m/s² × s
        self.vy += self.ay * dt_sim
        
        # Update position based on velocity
        self.x += self.vx * dt_sim  # m/s × s = m
        self.y += self.vy * dt_sim  # m/s × s = m

        # Calculate speed magnitude
        self.speed = sqrt(self.vx ** 2 + self.vy ** 2)  # m/s
        
        # Calculate force for display (converted to real-world units)
        self.printed_force = [0.0, 0.0]
        for f in self.attract_forces:
            self.printed_force[0] += f[0] / engine.gravity * engine.G
            self.printed_force[1] += f[1] / engine.gravity * engine.G
        
        # ===== INITIALIZATION =====
        # Initialize body on first update
        if not self.is_born and self in circles:
            self.birth_time = engine.net_simulation_time()
            
            # Apply random initial velocity if random mode enabled
            if engine.random_mode:
                # Total energy = energy per kg × mass
                total_energy = engine.random_energy_per_kg * self.mass

                # Maximum velocity based on E = 0.5 * m * v²
                max_velocity_per_frame = sqrt(2 * total_energy / self.mass)
                max_velocity = max_velocity_per_frame * engine.FPS_TARGET
                
                self.vx = random.uniform(-max_velocity, max_velocity)
                self.vy = random.uniform(-max_velocity, max_velocity)
            
            self.is_born = True
        
        # Update age (time since birth, excluding pause time)
        if self.birth_time is not None:
            self.age = engine.net_simulation_time() - self.birth_time
        
        # ===== UPDATE GEOMETRIC PROPERTIES =====
        self.surface = 4 * self.radius ** 2 * pi
        self.volume = 4 / 3 * pi * self.radius ** 3
        
        # Deselect if body is removed from simulation
        if self not in circles:
            self.is_selected = False
        
        # Update position tuple
        self.pos = (self.x, self.y)

    def draw_interpolated(self, screen, alpha, interpolate_radius: bool = True):
        """
        Draw body with interpolated position for smooth rendering.
        
        Uses linear interpolation between previous and current states
        for all visual properties (position, radius).
        
        Args:
            screen: Pygame screen surface
            alpha: Interpolation factor (0 = previous state, 1 = current state)
        """
        # Interpolate position between previous and current
        # This makes movement appear smooth even with fixed physics timestep
        # ===== GET INTERPOLATED STATE =====
        state = self.get_interpolated_state(alpha)
        
        world_x = state['x']
        world_y = state['y']
        if interpolate_radius:
            world_radius = state['radius']
        
        # ===== CONVERT WORLD → SCREEN =====
        screen_x, screen_y = engine.camera.world_to_screen(world_x, world_y)
        
        # ===== CALCULATE VISIBLE RADIUS =====
        # Apply camera scale to radius
        if interpolate_radius:
            screen_radius = world_radius * engine.camera.scale
        else:
            screen_radius = self.radius * engine.camera.scale
        visible_radius = max(1, int(screen_radius))
        
        # ===== SECURITY CHECKS =====
        if not isinstance(world_x, (int, float)):
            world_x = self.x
            warnings.warn(f"WARNING: Circle {self.number} had invalid x coordinate")
        
        if not isinstance(world_y, (int, float)):
            world_y = self.y
            warnings.warn(f"WARNING: Circle {self.number} had invalid y coordinate")
        
        if interpolate_radius:
            if not isinstance(world_radius, (int, float)):
                world_radius = self.radius
                warnings.warn(f"WARNING: Circle {self.number} had invalid radius")
        # ===========================
        
        # ===== CULLING (OPTIMIZATION) =====
        # Do not draw if out of screen (with margin)
        margin = visible_radius + 10
        if (screen_x < -margin or screen_x > screen.get_width() + margin or
            screen_y < -margin or screen_y > screen.get_height() + margin):
            return  # Out of screen, don't draw
            
        # ===== SELECTION HIGHLIGHTING =====
        if self.full_selected_mode:
            if self.is_selected:
                self.color = Display.DUCKY_GREEN
            else:
                if engine.screen_mode == "dark":
                    self.color = Display.WHITE
                elif engine.screen_mode == "light":
                    self.color = Display.BLACK
        else:
            if self.is_selected:
                if visible_radius <= 4:
                    pygame.draw.circle(screen, Display.DUCKY_GREEN, 
                                    (int(screen_x), int(screen_y)),
                                    visible_radius + 2)
                elif visible_radius <= 20:
                    pygame.draw.circle(screen, Display.DUCKY_GREEN, 
                                    (int(screen_x), int(screen_y)),
                                    visible_radius + visible_radius // 4 + 1)
                else:
                    pygame.draw.circle(screen, Display.DUCKY_GREEN, 
                                    (int(screen_x), int(screen_y)),
                                    visible_radius + 5)
        
        # ===== DRAW SHADOW/OUTLINE =====
        if not self.is_selected:
            if visible_radius <= 4:
                pygame.draw.circle(screen, Display.DARK_GREY, 
                                (int(screen_x), int(screen_y)), 
                                visible_radius + 1)
            elif visible_radius <= 20:
                pygame.draw.circle(screen, Display.DARK_GREY, 
                                (int(screen_x), int(screen_y)),
                                visible_radius + visible_radius // 5)
            else:
                pygame.draw.circle(screen, Display.DARK_GREY, 
                                (int(screen_x), int(screen_y)), 
                                visible_radius + 3)
        
        # ===== DRAW MAIN BODY CIRCLE =====
        self.rect = pygame.draw.circle(screen, self.color, 
                                    (int(screen_x), int(screen_y)), 
                                    visible_radius)

    def update_fusion(self, other):
        """
        Check and perform fusion with double verification.

        Checks TWO conditions:
        1. Visual collision detected (interpolated positions)
        2. Physical collision confirmed (real positions)
        """
        if not engine.fusions:
            return

        if self.mass < other.mass:
            return  # Only the heavier body can absorb

        # ===== PHYSICAL VERIFICATION (real positions) =====
        dx_real = other.x - self.x
        dy_real = other.y - self.y
        distance_real = sqrt(dx_real**2 + dy_real**2)

        physical_collision = distance_real <= (self.radius + other.radius)

        # ===== VISUAL VERIFICATION (interpolated positions) =====
        alpha = engine.current_alpha

        visual_x1 = self.prev_x + (self.x - self.prev_x) * alpha
        visual_y1 = self.prev_y + (self.y - self.prev_y) * alpha

        visual_x2 = other.prev_x + (other.x - other.prev_x) * alpha
        visual_y2 = other.prev_y + (other.y - other.prev_y) * alpha

        dx_visual = visual_x2 - visual_x1
        dy_visual = visual_y2 - visual_y1
        distance_visual = sqrt(dx_visual**2 + dy_visual**2)

        # Interpolated radius
        radius1 = self.prev_radius + (self.radius - self.prev_radius) * alpha
        radius2 = other.prev_radius + (other.radius - other.prev_radius) * alpha

        visual_collision = distance_visual <= (radius1 + radius2)

        # ===== FUSION IF BOTH CONDITIONS ARE TRUE =====
        if physical_collision and visual_collision:
            self.fusion(other)
        elif visual_collision and not physical_collision:
            # Visual collision detected but not physical collision
            # → Force a physics step (already handled by _check_visual_collisions)
            pass

    def fusion(self, other):
        """
        Merge two bodies, conserving momentum and mass.
        
        The larger body absorbs the smaller one. Position and velocity
        are calculated using center of mass and momentum conservation.
        
        IMPORTANT: Saves radius BEFORE fusion for smooth interpolation.
        
        Args:
            other: The other Circle object to merge with (will be destroyed)
        """
        # ===== SAVE CURRENT RADIUS BEFORE FUSION =====
        # This ensures smooth interpolation when radius suddenly increases
        self.prev_radius = self.radius

        # ===== CALCULATE TOTAL MASS =====
        total_mass = self.mass + other.mass
        
        # ===== CALCULATE NEW POSITION (CENTER OF MASS) =====
        # COM = (m1*r1 + m2*r2) / (m1 + m2)
        self.x = (self.x * self.mass + other.x * other.mass) / total_mass
        self.y = (self.y * self.mass + other.y * other.mass) / total_mass

        # ===== CALCULATE NEW VELOCITY (MOMENTUM CONSERVATION) =====
        # p = m*v, so v_new = (p1 + p2) / (m1 + m2)
        self.vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
        self.vy = (self.vy * self.mass + other.vy * other.mass) / total_mass

        # ===== UPDATE MASS =====
        self.mass = total_mass

        # ===== RECALCULATE RADIUS FROM NEW MASS (using density) =====
        if self.density > 0:
            volume = self.mass / self.density
            self.radius = ((3 * volume) / (4 * pi)) ** (1 / 3)
        else:
            # Fallback to default calculation if density is invalid
            self.radius = self.mass ** (1 / 3)
        
        # Note: prev_radius is already saved, so interpolation will smoothly
        # transition from old radius to new radius over next few frames

        # ===== MARK OTHER BODY FOR REMOVAL =====
        other.suicide = True

        # ===== INVALIDATE INTERPOLATION CACHE =====
        self._interpolated_cache['alpha'] = -1.0

    def is_colliding_with(self, other) -> bool:
        """
        Check if this body is colliding with another body.
        
        Collision is detected when the distance between centers is less than
        the sum of their radii (bodies are overlapping).
        
        Args:
            other: The other Circle object to check collision with
        
        Returns:
            True if bodies are colliding, False otherwise
        """
        # Calculate distance between centers
        dx = other.x - self.x
        dy = other.y - self.y
        distance = sqrt((dx ** 2) + (dy ** 2))

        # Collision if distance < sum of radii
        return distance < self.radius + other.radius


# -----------------
# class Engine
# -----------------
class Engine:
    def __init__(self):
        """
        Initialize the Gravity Engine simulation.
        
        Controls:
            - Space -> pause/unpause
            - Mouse wheel (optional) -> create the smallest bodies possible
            - V -> toggle velocity vectors
            - R -> toggle random_mode
            - G -> toggle reversed gravity
            - Left/Right/Wheel click -> hold to create bodies
                                    -> select/deselect body
            - Delete -> Delete selected body
        """

        # ==================== FILE MANAGER ====================    
        self.fm = FileManager(
            project_name="GravityEngine",
            project_root="GravityEngine",
            dev_data_folder="user_data",
            use_documents=True
        )
        
        # Create necessary folders
        self.screenshots_folder_path = self.fm.create_folder('screenshots')
        self.saves_folder_path = self.fm.create_folder('saves')
        self.logs_folder_path = self.fm.create_folder('logs')

        # ==================== SPLASH SCREEN SETTINGS ====================
        self.splash_screen_font = self.fm.resource_path('assets/fonts/main_font.ttf')
        self.splash_screen_enabled = True  # Enable/disable splash screen
        self.splash_screen_duration = 3.0  # Duration in seconds (can be adjusted)
        self.author_first_name = "Nils"  # Your first name
        self.author_last_name = "DONTOT"  # Your last name
        self.project_version = "3.4.0"
        self.project_description = f"Gravity Engine v{self.project_version} - A celestial body simulation"  # Project description
        
        # ==================== DISPLAY SETTINGS ====================
        self.FULLSCREEN = True
        self.screen_mode: str = "dark"  # "dark" or "light"
        
        WIDTH: int = 0
        HEIGHT: int = 0
        
        # Initialize screen
        self.info = pygame.display.Info()
        screen_size: tuple[int, int] = (self.info.current_w, self.info.current_h)
        available_screen_modes: list[tuple[int, int]] = pygame.display.list_modes()
        
        if self.FULLSCREEN:
            self.screen = pygame.display.set_mode(available_screen_modes[0], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        pygame.display.set_caption(f'Gravity Engine {self.project_version} by {self.author_first_name} {self.author_last_name}')

        # ==================== TIMESTEP SETTINGS ====================
        # FPS number targeted
        self.FPS_TARGET = 120
        
        # Fixed timestep for physics (ensures determinism)
        self.physics_timestep = 1.0 / self.FPS_TARGET  # 1/120 s = 0.00833 s
        
        # Time accumulator - accumulates real time until we can do a physics step
        self.time_accumulator = 0.0
        
        # Max accumulated time (prevents "spiral of death")
        # If accumulator > max_accumulation, clamp it to prevent infinite loop
        self.max_accumulation = 0.25  # 250 ms max (30 physics steps)
        
        # Previous frame time for delta calculation
        self.previous_time = time.time()

        # ==================== SIMULATION SETTINGS ====================
        self.FPS_TARGET = 120
        self.time_acceleration = 2e4  # Time acceleration factor
        self.growing_speed = 0.1   # Body growth speed when creating
        
        # ==================== UI SETTINGS ====================
        self.used_font = self.fm.resource_path('assets/fonts/main_font.ttf')
        self.txt_size = 30
        self.txt_gap: int = 15
        self.font = pygame.font.Font(self.used_font, self.txt_size)
        self.info_y: int = 20
        
        # Temporary texts
        self.temp_texts: list[TempText] = []
        
        # ==================== PHYSICS SETTINGS ====================
        self.G = 6.6743e-11
        self.default_gravity = self.G
        self.gravity: float = self.default_gravity
        self.fusions = True

        self.minimum_mass = 1e3  # in kg
        
        # Default density for new bodies (mass per unit volume)
        # This determines how large a body will be for a given mass
        self.default_density = 5.514e3  # 1000 <=> 1000 kg/m^3, by default on 5.514 (Earth density)

        self.use_interpolation = True
        
        # ==================== VISUALIZATION SETTINGS ====================
        self.vectors_printed = False
        self.force_vectors = True
        self.cardinal_vectors = False
        self.vectors_in_front = True
        self.vector_scale = 1

        # ==================== PERFORMANCE MODE ====================
        self.performance_mode = "precise"  # "precise" or "adaptive", "adaptive" as actually important problems
        # - "precise": Slows down if CPU is slow (deterministic)
        # - "adaptive": Compensates with large steps (smooth but imprecise)
        # Maximum allowed step time in adaptive performance mode (prevents overly large physics steps)
        self.MAX_ADAPTIVE_STEP_TIME = 0.050  # Max 50ms

        # Adaptive throttling: limits the frequency of physics calculations
        self.min_physics_interval = 0.025  # 200ms = max 5 calculations/second
        self.last_physics_time = 0.0  # Timestamp of the last physics calculation
        self.physics_time_debt = 0.0  # Time accumulated since the last calculation

        # ==================== RENDERING STATE ====================
        self.current_alpha = 1.0  # Current interpolation alpha (for selection)
        
        # ==================== RANDOM GENERATION SETTINGS ====================
        self.random_mode = False
        
        # Define max random energy in Joules
        self.random_energy_per_kg = 1e-8  # J/kg

        # in kg, random beteween self.minimum_mass and value
        self.random_mass_field = 1e7  # (for camera.scale = 1.0)

        self.random_environment_number: int = 20
        
        # ==================== AUDIO SETTINGS ====================
        self.musics_folder_path = "../'assets/musics"  # without ressource_path() because it is a folder
        self.music = False
        self.music_volume = 1
        
        # ==================== SIMULATION STATE ====================
        self.is_paused = False
        self.reversed_gravity = False
        
        # Performance tracking
        self.displayed_FPS = self.FPS_TARGET
        self.frequency = self.FPS_TARGET
        self.latency = None
        self.save_time_1 = 0
        self.save_time_2 = 0
        self.counter = 0

        # ==================== SIMULATION TIME ====================
        # time tracking
        self.simulation_time = 0.0  # Actual simulation time calculated (in seconds)
        self.simulation_time_in_pause = 0.0  # Time spent paused (towards simulation_time)
        self.pause_start_simulation_time = None  # simulation_time at the moment of pause

        # ==================== GESTION VISUELLE DES COLLISIONS ====================
        self.skip_prev_update = False  # Drapeau pour empêcher la mise à jour de prev_x/prev_y
        
        # ==================== BODY MANAGEMENT ====================
        self.circle_number = 0
        self.circle_selected = False

        # ==================== CAMERA ====================
        self.camera_basic_scale = 1.0
        self.camera_scale_factor = 1.1  # 1.1 or exp(0.05)
        self.camera = Camera(
                            x=0.0,
                            y=0.0,
                            scale=self.camera_basic_scale,
                            scale_step=self.camera_scale_factor
                        )
        self.camera_speed = 10

        # ==================== INPUT HANDLING ====================
        self.inputs: dict = {}
        self.INPUT_MAP = {}
        self.MOUSEBUTTON_MAP = {}
        self.show_help = False
        
        # Mouse interaction state
        self.mouse_down = False
        self.mouse_down_start_time = None  # Timestamp when mouse button was pressed
        self.can_create_circle = True
        self.circle_collided = False
        self.collision_detected = False
        self.temp_circle: Circle

    def handle_input(self, event: pygame.event.Event = None) -> None:
        """
        Handle keyboard input events.
        
        Records key press and release events in the inputs dictionary.
        Note: Currently both KEYDOWN and KEYUP set the same value (True).
        
        Args:
            event: Pygame event object containing input information
        """
        if event.type is pygame.KEYDOWN:
            self.inputs[event.key] = True
        elif event.type is pygame.KEYUP:
            self.inputs[event.key] = True

    def refresh_pause(self):
        
        """Update accumulated pause time.
        
        Called continuously while paused to track total time spent in pause state.
        This ensures accurate time tracking when calculating simulation age."""
        
        self.simulation_time_in_pause += time.time() - self.pause_start_simulation_time
        self.pause_start_simulation_time = time.time()

    def pause(self):
        """
        Pause the simulation.
        
        Stops physics updates while keeping the display active.
        Records the pause start time for accurate time tracking.
        """
        self.pause_start_simulation_time = time.time()
        self.pause_start_simulation_time = self.net_simulation_time()  # Save simulation_time
        self.is_paused = True

    def unpause(self):
        """
        Resume the simulation.
        
        Updates time tracking for all bodies and the engine to account for
        the time spent in pause state. This ensures age calculations remain accurate.
        """
        # Update pause time for real time
        self.simulation_time_in_pause += time.time() - self.pause_start_simulation_time
        
        # Update pause time for simulation time
        # (While paused, simulation_time does not change, so there is no need to adjust it)
        
        # Clear pause state
        self.pause_start_simulation_time = None
        self.pause_start_simulation_time = None
        self.is_paused = False

    def net_simulation_time(self) -> float:
        """
        Return simulation time (based on physics steps executed, not real time).
        
        This ensures the simulation clock advances at the same rate as physics.
        """
        return self.simulation_time

    def brut_age(self) -> float:
        """
        Return total elapsed time since simulation start.
        
        Includes time spent in pause state.
        
        Returns:
            Total elapsed time in seconds
        """
        age = time.time() - self.beginning_time
        return age

    def select_circle(self, number: int) -> None:
        """
        Select a body by its unique number.
        
        Searches for a body with the given number and selects it.
        If not found, displays an error message.
        
        Args:
            number: The unique identifier of the body to select
        """
        for circle in circles:
            if circle.number == number:
                circle.is_selected = True
                self.circle_selected = True
                return None
        # Display error message if body not found
        TempText(f"Body n°{number} does not exist", 3)

    def print_global_info(self, y):
        """
        Display global simulation information on screen.
        
        Shows statistics about the simulation including:
        - Body count and total mass
        - Heaviest and oldest bodies
        - Simulation age and time factor
        - Current settings (gravity, vectors, random mode)
        - Performance metrics (FPS)
        
        Args:
            y: Y-coordinate for the top of the info panel
        """
        # Display heaviest body information
        heaviest_tuple = Utils.heaviest()
        if heaviest_tuple is not None:
            text = f"Heaviest body : n°{heaviest_tuple[0]} -> {heaviest_tuple[1] / 1000:.2e} kg"
            Utils.write_screen(text, (20, y), Display.BLUE, 2)
        else:
            text = f"Heaviest body : None"
            Utils.write_screen(text, (20, y), Display.BLUE, 2)

        # Show delete instruction when a body is selected
        if self.circle_selected and len(circles) > 0:
            Utils.write_screen(f"Delete : Delete key", (
                int((self.screen.get_width() / 2) - (self.font.size("Delete : Delete key")[0] / 2)),
                y), Display.BLUE, 0)

        text = "Hold H or I to display the help box"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Color(150, 0, 0), 0)

        # Display reversed gravity status (top right)
        if self.reversed_gravity:
            text = f"Reversed gravity : Enabled"
        else:
            text = f"Reversed gravity : Disabled"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Display.BLUE, 2)

        # Display velocity vectors status (top right)
        if self.vectors_printed:
            text = f"Vectors : Enabled"
        else:
            text = f"Vectors : Disabled"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Display.BLUE, 3)

        # Display random mode status (top right)
        if self.random_mode:
            text = f"Random mode : Enabled"
        else:
            text = f"Random mode : Disabled"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Display.BLUE, 4)

        # Display time acceleration factor (bottom right)
        text = f"Time factor : ×{self.time_acceleration:.2e}"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - 2 * self.txt_size - self.txt_gap), Display.BLUE, 0)

        # Display camera zoom (bottom right)
        text = f"Camera zoom : ×{self.camera.scale:.2e}"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - 3 * self.txt_size - 2 * self.txt_gap), Display.BLUE, 0)

        # Display pause status (bottom right)
        if self.is_paused:
            text = f"Pause : Enabled"
        else:
            text = f"Pause : Disabled"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - self.txt_size), Display.BLUE, 0)

        # Display body count (top left)
        text = f"Number of bodies : {len(circles)}"
        Utils.write_screen(text, (20, y), Display.BLUE, 0)

        # Display total mass (top left)
        text = f"Total mass : {round(Utils.mass_sum()):.2e} kg"
        Utils.write_screen(text, (20, y), Display.BLUE, 1)

        # Display oldest body information (top left)
        oldest_tuple = Utils.oldest()
        if oldest_tuple is not None:
            # Convert age to years (31,557,600 seconds per year)
            oldest_age_years = oldest_tuple[1] * engine.time_acceleration / 31_557_600
            if oldest_age_years < 2:
                text = f"Oldest body : n°{oldest_tuple[0]} -> {int(oldest_age_years * 1000) / 1000} Earth year"
                Utils.write_screen(text, (20, y), Display.BLUE, 3)
            else:
                text = f"Oldest body : n°{oldest_tuple[0]} -> {int(oldest_age_years * 1000) / 1000} Earth years"
                Utils.write_screen(text, (20, y), Display.BLUE, 3)
        else:
            text = f"Oldest body : None"
            Utils.write_screen(text, (20, y), Display.BLUE, 3)

        # Display simulation age (bottom left)
        sim_age_years = self.net_simulation_time() * engine.time_acceleration / 31_557_600
        if sim_age_years < 2:
            text = f"Simulation age : {int(sim_age_years * 1000) / 1000} Earth year"
            Utils.write_screen(text, (20, self.screen.get_height() - 20 - engine.txt_size), Display.BLUE, 0)
        else:
            text = f"Simulation age : {int(sim_age_years * 1000) / 1000} Earth years"
            Utils.write_screen(text, (20, self.screen.get_height() - 20 - engine.txt_size), Display.BLUE, 0)

        # Display FPS (bottom center)
        text = f"FPS : {round(self.displayed_FPS)}"
        Utils.write_screen(text, (int((self.screen.get_width() / 2) - (self.font.size(text)[0] / 2)),
                          int(self.screen.get_height() - 20 - engine.txt_size)), Display.BLUE, 0)

    def show_help_overlay(self):
        """
        Display help overlay with all keyboard and mouse controls.
        
        Shows a semi-transparent overlay with comprehensive control information.
        Can be toggled on/off with H or I key.
        
        Uses Utils.write_screen() for consistent text rendering with smaller font size.
        """
        # Create semi-transparent overlay
        self.screen.fill((20, 20, 20, 200))
        
        # ===== SAVE CURRENT FONT AND CREATE SMALLER FONT =====
        original_font = self.font
        original_txt_size = self.txt_size
        original_txt_gap = self.txt_gap
        
        self.txt_size = 20  # Smaller text for help overlay
        self.txt_gap = 5    # Smaller gap for compact display
        self.font = pygame.font.Font(self.used_font, self.txt_size)
        
        # Calculate positions
        center_x = self.screen.get_width() // 2
        left_margin = center_x - 350
        key_col_x = center_x - 330
        sep_col_x = center_x - 120
        desc_col_x = center_x - 80
        start_y = 80
        
        # ===== TITLE =====
        title = "GRAVITY ENGINE - CONTROLS GUIDE"
        title_font = pygame.font.Font(self.used_font, 32)
        title_surface = title_font.render(title, True, Display.DUCKY_GREEN)
        title_rect = title_surface.get_rect(center=(center_x, start_y))
        self.screen.blit(title_surface, title_rect)
        
        # Draw separator line
        pygame.draw.rect(self.screen, Display.BLUE, 
                        (center_x - 300, start_y + 35, 600, 3))
        
        # ===== CONTROLS SECTIONS =====
        sections = [
            {
                "title": "MOUSE CONTROLS",
                "controls": [
                    ("Left Click", "Select body / Create body (on empty space)"),
                    ("Left Hold", "Increase body size exponentially"),
                    ("Right Click + Drag", "Pan camera view"),
                    ("Mouse Wheel ↑", "Zoom in (centered on cursor)"),
                    ("Mouse Wheel ↓", "Zoom out (centered on cursor)"),
                ]
            },
            {
                "title": "KEYBOARD CONTROLS",
                "controls": [
                    ("T", "Reset camera to default position and zoom"),
                    ("A", "Zoom in (screen-centered)"),
                    ("E", "Zoom out (screen-centered)"),
                    ("↑ ← ↓ →", "Pan camera with arrow keys"),
                    ("", ""),
                    ("Space", "Pause / Unpause simulation"),
                    ("V", "Toggle velocity vectors display"),
                    ("R", "Toggle random velocity mode (mass-proportional)"),
                    ("G", "Toggle reversed gravity (repulsion)"),
                    ("P", f"Generate random environment ({self.random_environment_number} bodies, zoom-adaptive)"),
                    ("S", "Take a screenshot"), ("", f"Saved in {self.screenshots_folder_path}"),
                    ("Delete", "Delete selected body"),
                    ("H / I", "Toggle this help overlay"),
                    ("Escape", "Exit program"),
                ]
            },
        ]
        
        # Starting Y position and line counter
        base_y = start_y + 60
        current_line = 0
        
        # Render each section
        for section in sections:
            # Section title
            Utils.write_screen(
                section["title"],
                (left_margin, base_y),
                Display.BLUE,
                current_line
            )
            current_line += 1
            
            # Section controls
            for key, description in section["controls"]:
                y_pos = base_y + current_line * (self.txt_gap + self.txt_size)
                current_line += 1
                if (key, description) == ("", ""):
                    continue
                
                # Key (green, left column)
                key_surface = self.font.render(key, True, Display.DUCKY_GREEN)
                self.screen.blit(key_surface, (key_col_x, y_pos))
                
                # Separator arrow (grey)
                sep_surface = self.font.render("→", True, Display.DARK_GREY)
                self.screen.blit(sep_surface, (sep_col_x, y_pos))
                
                # Description (white, right column)
                desc_surface = self.font.render(description, True, Display.WHITE)
                self.screen.blit(desc_surface, (desc_col_x, y_pos))
            
            # Spacing between sections
            current_line += 1
        
        # ===== FOOTER =====
        footer_y = self.screen.get_height() - 50
        
        # Version and author (centered, grey)
        footer_text = f"Gravity Engine v{self.project_version} by {self.author_first_name} {self.author_last_name}"
        footer_x = center_x - self.font.size(footer_text)[0] // 2
        Utils.write_screen(footer_text, (footer_x, footer_y), Display.DARK_GREY, 0)
        
        # Close instruction (centered, blue)
        close_text = "Release H or I to close"
        close_x = center_x - self.font.size(close_text)[0] // 2
        Utils.write_screen(close_text, (close_x, footer_y), Display.BLUE, 1)
        
        # ===== RESTORE ORIGINAL FONT SETTINGS =====
        self.font = original_font
        self.txt_size = original_txt_size
        self.txt_gap = original_txt_gap

    def generate_environment(self, count: int = 50, temptext: bool = False):
        """
        Generate a random environment with multiple bodies.
        
        Bodies are spawned across the visible world area,
        with masses proportional to the camera zoom level.

        Args:
            count: Ignored parameter, kept for compatibility.
        """
        count = self.random_environment_number
        
        # ===== CALCULATE VISIBLE WORLD AREA =====
        # Top-left corner of the screen in world coordinates
        world_x_min, world_y_min = self.camera.screen_to_world(0, 0)
        
        # Bottom-right corner of the screen in world coordinates
        world_x_max, world_y_max = self.camera.screen_to_world(
            self.screen.get_width(),
            self.screen.get_height()
        )
        
        # ===== CALCULATE MASS RANGE BASED ON ZOOM =====
        # The more you zoom out, the more massive the bodies must be to remain visible
        zoom_factor = self.camera.scale  # 1.0 = normal, 0.1 = very zoomed out
        
        # Adjust the mass range inversely to the zoom
        # Zoom 1.0 -> normal mass
        # Zoom 0.1 -> mass ×10
        # Zoom 10.0 -> mass /10
        mass_multiplier = 1.0 / zoom_factor ** 2
        
        min_mass = self.minimum_mass * mass_multiplier
        max_mass = self.random_mass_field * mass_multiplier
        
        # ===== GENERATE BODIES =====
        for _ in range(count):
            # Random position in the visible world space
            world_x = random.uniform(world_x_min, world_x_max)
            world_y = random.uniform(world_y_min, world_y_max)
            
            # Random mass adapted to the zoom
            # Masse selon distribution logarithmique
            log_min = log10(min_mass)
            log_max = log10(max_mass)
            log_mass = random.uniform(log_min, log_max)
            mass = 10 ** log_mass
            
            new = Circle(
                x=world_x,
                y=world_y,
                density=self.default_density,
                mass=mass
            )
            circles.append(new)
        
        # ===== USER FEEDBACK =====
        if temptext:
            TempText(
                f"Generated {count} bodies (zoom: {zoom_factor:.2e}x)",
                2.0,
                (int((self.screen.get_width() / 2) - 200),
                self.info_y - self.txt_gap - self.txt_size),
                line=2
            )

    def get_frequency(self) -> float:
        """
        Calculate and return current frame frequency (FPS).
        
        Frequency is the inverse of latency (time between frames).
        
        Returns:
            Current frame frequency in Hz (frames per second)
        """
        frequency = 1 / self.get_latency()
        self.save_time_1 = time.time()
        return frequency

    def get_latency(self) -> float:
        """
        Calculate and return latency since last frame.
        
        Measures the time elapsed since the last call to this method.
        Updates internal timestamp for next calculation.
        
        Returns:
            Latency in seconds (time between frames)
        """
        latency = time.time() - self.save_time_2
        self.save_time_2 = time.time()
        return latency

    def handle_music(self, loop: int = 0, start: float = 0, fade_ms: int = 0):
        """
        Handle background music playback.
        
        Automatically loads and plays music files when music is enabled and
        no music is currently playing. Queues multiple tracks for continuous playback.
        
        Args:
            loop: Number of times to loop (-1 for infinite)
            start: Starting position in seconds
            fade_ms: Fade-in duration in milliseconds
        """
        if not pygame.mixer.music.get_busy() and self.music:
            try:
                # Load and queue music tracks
                pygame.mixer.music.load(self.fm.ressource_path(f'{self.musics_folder_path}/music1.mp3'))
                pygame.mixer.music.queue(self.fm.ressoucre_path(f'{self.musics_folder_path}/music2.mp3'))
                pygame.mixer.music.queue(self.fm.ressource_path(f'{self.musics_folder_path}/music3.mp3'))
            except FileNotFoundError:
                # Silently fail if music files don't exist
                pass
            pygame.mixer.music.play(loop, start, fade_ms)
    
    def physics_step(self, dt):
        """
        Execute one physics step with fixed timestep.
        
        This ensures deterministic physics regardless of rendering FPS.
        Always called with dt = self.physics_timestep (1/120 s).
        
        Args:
            dt: Fixed timestep duration (always self.physics_timestep)
        """
        # Remove bodies marked for deletion (after fusion)
        circles_to_remove = [circle for circle in circles if circle.suicide]
        for circle in circles_to_remove:
            circles.remove(circle)
        
        # Calculate gravitational forces between all body pairs
        for circle in circles:
            circle.attract_forces = []  # Reset force list
            for other_circle in circles:
                if circle != other_circle:
                    # Calculate and store attraction force
                    circle.attract_forces.append(circle.attract(other_circle))
                    # Check for fusion conditions
                    circle.update_fusion(other_circle)
        
        # Update all bodies (position, velocity, age, etc.)
        for circle in circles:
            circle.physics_update(dt)

        # IMPORTANT: Increment simulation time
        self.simulation_time += dt
    
    def render(self, alpha):
        """
        Render the current frame with interpolation for smooth display.
        
        Uses interpolation between previous and current physics states
        to ensure smooth rendering even when physics runs at fixed timestep.
        
        Args:
            alpha: Interpolation factor (0 to 1) between physics states
                0 = exactly at previous state
                1 = exactly at current state
        """
        if self.use_interpolation and self._check_visual_collisions(alpha):
            # Visual collision detected!
        
            # STEP 1: Save the current VISUAL positions
            for circle in circles:
                # Position where the body is CURRENTLY visually displayed
                visual_x = circle.prev_x + (circle.x - circle.prev_x) * alpha
                visual_y = circle.prev_y + (circle.y - circle.prev_y) * alpha
                
                # Temporarily store
                circle._visual_x = visual_x
                circle._visual_y = visual_y
            
            self.skip_prev_update = True

            # STEP 2: Perform the physics calculation
            if self.time_accumulator > 0:
                self.physics_step(self.time_accumulator)
                self.time_accumulator = 0
            
            self.skip_prev_update = False
            
            # STEP 3: Use the visual positions as new "prev"
            for circle in circles:
                if hasattr(circle, '_visual_x'):
                    circle.prev_x = circle._visual_x
                    circle.prev_y = circle._visual_y
                    # Clean up
                    delattr(circle, '_visual_x')
                    delattr(circle, '_visual_y')
        
            # STEP 4: Reset alpha to 0 (start again from the saved visual position)
            alpha = 0

        # Render vectors if enabled
        if self.vectors_in_front:
            # Bodies first, then vectors on top
            for circle in circles:
                circle.draw_interpolated(self.screen, alpha)
            if self.vectors_printed:
                for circle in circles:
                    circle.print_global_speed_vector(False, alpha)
                    if self.force_vectors:
                        circle.print_force_vector(False, alpha)
                    
        else:
            # Vectors first, then bodies on top
            if self.vectors_printed:
                for circle in circles:
                    circle.print_global_speed_vector(False ,alpha)
                    if self.force_vectors:
                        circle.print_force_vector(False, alpha)
                    
            for circle in circles:
                circle.draw_interpolated(self.screen, alpha)
        
        # Draw temporary body being created
        if self.temp_circle:
            self.temp_circle.draw_interpolated(self.screen, alpha, interpolate_radius=False)
        
        # Display UI information
        if not self.show_help:
            self.print_global_info(self.info_y)
            for circle in circles:
                if circle.is_selected:
                    circle.print_info(circle.info_y)
        else:
            self.show_help_overlay()

    def _check_visual_collisions(self, alpha):
        """Check if any bodies collide at interpolated positions."""
        for i, circle in enumerate(circles):
            if circle.suicide:
                continue
            
            # Position interpolée
            x1 = circle.prev_x + (circle.x - circle.prev_x) * alpha
            y1 = circle.prev_y + (circle.y - circle.prev_y) * alpha
            
            for other in circles[i+1:]:
                if other.suicide:
                    continue
                
                # Position interpolée de l'autre
                x2 = other.prev_x + (other.x - other.prev_x) * alpha
                y2 = other.prev_y + (other.y - other.prev_y) * alpha
                
                # Distance
                dx = x2 - x1
                dy = y2 - y1
                dist = sqrt(dx*dx + dy*dy)
                
                # Collision ?
                if dist <= circle.radius + other.radius:
                    return True
        
        return False

    def show_splash_screen(self):
        """
        Display a splash screen at startup with author information and project description.
        
        The splash screen blocks all interactions for the configured duration.
        """
        if not self.splash_screen_enabled:
            return
        
        # Create a clock for timing
        clock = pygame.time.Clock()
        start_time = time.time()
        
        # Create a larger font for the splash screen
        splash_font_large = pygame.font.Font(self.splash_screen_font, 60)
        splash_font_medium = pygame.font.Font(self.splash_screen_font, 40)
        splash_font_small = pygame.font.Font(self.splash_screen_font, 30)
        
        # Main splash screen loop
        running = True
        while running:
            # Calculate elapsed time
            elapsed = time.time() - start_time
            
            # Check if duration has passed
            if elapsed >= self.splash_screen_duration:
                running = False
                break
            
            # Fill screen with background color
            if self.screen_mode == "dark":
                self.screen.fill(Display.BLACK)
            else:
                self.screen.fill(Display.WHITE)
            
            # Calculate center positions
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            
            # Render author name (first name + last name)
            author_text = f"{self.author_first_name} {self.author_last_name}"
            author_surface = splash_font_large.render(author_text, True, Display.BLUE)
            author_rect = author_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 80))
            self.screen.blit(author_surface, author_rect)
            
            # Render project description
            desc_surface = splash_font_medium.render(self.project_description, True, Display.BLUE)
            desc_rect = desc_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            self.screen.blit(desc_surface, desc_rect)
            
            # Render copyright/version info (optional)
            version_text = "Copyright (c) 2026"
            version_surface = splash_font_small.render(version_text, True, Display.DARK_GREY)
            version_rect = version_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 60))
            self.screen.blit(version_surface, version_rect)
            
            # Update display
            pygame.display.flip()
            
            # Process events (but ignore all input)
            for event in pygame.event.get():
                # Ignore all events during splash screen
                if event.type == pygame.QUIT:
                    # Allow quit to work
                    pygame.quit()
                    sys.exit()
                # All other events are ignored
            
            # Maintain FPS
            clock.tick(self.FPS_TARGET)
        
        # Clear the screen after splash
        if self.screen_mode == "dark":
            self.screen.fill(Display.BLACK)
        else:
            self.screen.fill(Display.WHITE)
        pygame.display.flip()

    def run(self):
        """
        Launch the main simulation loop.
        
        This is the core game loop that handles:
        - Event processing (keyboard, mouse, window events)
        - Physics simulation (gravitational forces, collisions, fusion)
        - Rendering (bodies, vectors, UI)
        - State management (pause, selection, body creation)
        
        The loop runs at the target FPS and continues until the window is closed.
        """
        # ==================== MINIMUM DEBUG ====================
        Tester.default_debug()

        # Show splash screen at startup
        self.show_splash_screen()
        
        # Initialize music volume
        pygame.mixer.music.set_volume(self.music_volume)

        # Initialize global body list
        global circles
        circles = []

        # Initialize mouse interaction state
        self.temp_circle = None
        self.mouse_down = False
        self.mouse_down_start_time = None

        # Create clock for FPS control
        clock = pygame.time.Clock()

        # Initialize selection state
        self.circle_selected = False

        # Map keyboard keys to actions
        self.KEY_MAP = {
            pygame.K_SPACE: ActionManager.toggle_pause,
            pygame.K_v: ActionManager.toggle_vectors_printed,
            pygame.K_r: ActionManager.toggle_random_mode,
            pygame.K_g: ActionManager.toggle_reversed_gravity,
            pygame.K_p: self.generate_environment,
            pygame.K_DELETE: ActionManager.delete_selected_circle,
            pygame.K_ESCAPE: ActionManager.quit_engine,
            # ===== CAMERA =====
            pygame.K_a: ActionManager.zoom_in,      # A to zoom in
            pygame.K_e: ActionManager.zoom_out,    # E to zoom out
            pygame.K_t: ActionManager.reset_camera,    # T to reset
            # Arrows to move
            pygame.K_LEFT: lambda: ActionManager.pan_camera(self.camera_speed, 0),
            pygame.K_RIGHT: lambda: ActionManager.pan_camera(-self.camera_speed, 0),
            pygame.K_UP: lambda: ActionManager.pan_camera(0, self.camera_speed),
            pygame.K_DOWN: lambda: ActionManager.pan_camera(0, -self.camera_speed),
            # Take screenshots
            pygame.K_s: ActionManager.save_screenshot
        }
        
        # Map mouse events to actions
        self.MOUSEBUTTON_MAP = {
            pygame.MOUSEBUTTONDOWN: ActionManager.handle_mouse_button_down,
            pygame.MOUSEBUTTONUP: ActionManager.handle_mouse_button_up,
        }

        running = True

        # Initialize time tracking
        self.previous_time = time.time()
        self.time_accumulator = 0.0

        # ======== MAIN LOOP ========
        while running:
            # ===== TIMING =====
            current_time = time.time()
            frame_time = current_time - self.previous_time
            self.previous_time = current_time
            
            # Update performance metrics (for display)
            self.frequency = 1.0 / frame_time if frame_time > 0 else self.FPS_TARGET
            self.latency = frame_time
            
            # Update FPS display at regular intervals
            if self.counter / self.frequency == int(self.counter / self.frequency):
                if self.frequency < self.FPS_TARGET + 20:
                    self.displayed_FPS = self.frequency
                else:
                    self.displayed_FPS = self.FPS_TARGET
            
            # Update frame counter
            if self.counter + 1 >= self.frequency:
                self.counter = 0
            else:
                self.counter += 1
            
            # Add to accumulator (only if not paused)
            if not self.is_paused:
                self.time_accumulator += frame_time
            
            # Limit accumulator to prevent spiral of death
            if self.time_accumulator > self.max_accumulation:
                self.time_accumulator = self.max_accumulation
            
            # ===== EVENT HANDLING =====
            for event in pygame.event.get():
                self.handle_input(event)
                
                if event.type == pygame.QUIT:
                    ActionManager.quit_engine()
                elif event.type in self.MOUSEBUTTON_MAP:
                    action = self.MOUSEBUTTON_MAP.get(event.type)
                    if action:
                        action(event)
                elif event.type == pygame.KEYDOWN:
                    action = self.KEY_MAP.get(event.key)
                    if action:
                        action()

            # ===== CHECK HELP KEYS (HOLD TO DISPLAY) =====
            keys = pygame.key.get_pressed()
            self.show_help = keys[pygame.K_h] or keys[pygame.K_i]

            # ===== PAN CAMERA =====
            if engine.camera.is_panning:
                mx, my = pygame.mouse.get_pos()
                engine.camera.update_pan(mx, my)
            
            # ===== SELECTION MANAGEMENT =====
            # Ensure only one body is selected at a time
            for circle in circles:
                if circle.is_selected:
                    self.circle_selected = True
                    for other in circles:
                        if circle != other:
                            other.is_selected = False
                    break
                else:
                    self.circle_selected = False
            
            # ===== MOUSE HOLD BEHAVIOR (body creation) =====
            if self.mouse_down and self.temp_circle:
                if self.mouse_down_start_time is not None:
                    time_held = time.time() - self.mouse_down_start_time
                else:
                    time_held = 0
                    self.mouse_down_start_time = time.time()

                # ===== SAVE PREVIOUS RADIUS BEFORE MODIFICATION =====
                # This ensures smooth interpolation during growth
                self.temp_circle.prev_radius = self.temp_circle.radius

                # ===== CALCULATE GROWTH RATE =====
                acceleration_factor = exp(time_held * 0.8)
                
                # Growth in screen pixels
                # Number of pixels per frame
                screen_pixels_per_frame = self.growing_speed * 100 * frame_time * acceleration_factor
                # Convert to world meters
                world_meters_per_frame = screen_pixels_per_frame / self.camera.scale
                # Apply the growth
                self.temp_circle.radius += world_meters_per_frame
                
                # ===== RECALCULATE MASS ===== (from radius and density)
                if self.temp_circle.density > 0:
                    volume = (4 / 3) * pi * (self.temp_circle.radius ** 3)
                    self.temp_circle.mass = self.temp_circle.density * volume
                else:
                    self.temp_circle.mass = self.temp_circle.radius ** 3

                # ===== INVALIDATE INTERPOLATION CACHE =====
                self.temp_circle._interpolated_cache['alpha'] = -1.0
                
                # ===== CHECK COLLISION =====
                self.collision_detected = False
                for circle in circles:
                    if self.temp_circle.is_colliding_with(circle):
                        self.collision_detected = True
                        break
                
                if self.collision_detected:
                    circles.append(self.temp_circle)
                    self.temp_circle = None
                    self.mouse_down = False
                    self.mouse_down_start_time = None
            
            # ===== PHYSICS (fixed timestep) =====
            # Do as many physics steps as needed to catch up
            if not self.is_paused:
                current_real_time = time.time()
        
                if self.performance_mode == "adaptive":
                    # ADAPTIVE mode: limit the frequency of physics calculations for performance

                    time_since_last_physics = current_real_time - self.last_physics_time

                    # Accumulate time since last physics update
                    self.physics_time_debt += frame_time

                    # Check if enough time has passed to perform a physics update
                    if time_since_last_physics >= self.min_physics_interval:
                        # Perform ONLY ONE physics calculation with all the accumulated time
                        total_dt = self.physics_time_debt

                        # Limit the maximum step size to avoid "physics explosions" (instabilities/bugs from too large time step)
                        max_single_step = 0.5  # maximum of 500ms per step
                        if total_dt > max_single_step:
                            warnings.warn(f"WARNING: Physics step too large ({total_dt*1000:.0f}ms), clamping to {max_single_step*1000:.0f}ms")
                            total_dt = max_single_step

                        # Execute the physics update
                        self.physics_step(total_dt)

                        # Reset counters for next calculation and for interpolation rendering
                        self.last_physics_time = current_real_time
                        self.physics_time_debt = 0.0
                        self.time_accumulator = 0.0  # Reset for interpolation

                    else:
                        # Pas encore temps de calculer, juste accumuler pour l'interpolation
                        self.time_accumulator += frame_time
                        
                        # Limiter l'accumulator pour éviter débordement
                        if self.time_accumulator > self.min_physics_interval:
                            self.time_accumulator = self.min_physics_interval
                
                elif self.performance_mode == "precise":
                    # Mode précis : comportement original (calculs réguliers)
                    self.time_accumulator += frame_time
                    
                    # Limiter accumulator
                    if self.time_accumulator > self.max_accumulation:
                        self.time_accumulator = self.max_accumulation
                    
                    # Faire autant de calculs que nécessaire
                    physics_steps = 0
                    max_steps_per_frame = 2
                    
                    while self.time_accumulator >= self.physics_timestep:
                        if physics_steps >= max_steps_per_frame:
                            break
                        
                        self.physics_step(self.physics_timestep)
                        self.time_accumulator -= self.physics_timestep
                        physics_steps += 1
                    
                    # Perdre le temps restant si limite atteinte
                    if physics_steps >= max_steps_per_frame:
                        self.time_accumulator = 0.0

                else:
                    # when performance_mode is not "precise" or "adaptative"
                    raise ValueError("Engine.performance_mode must be \"precise\" or \"adaptive\" [can be updated in Engine.__init__()]")
            
            # ===== RENDERING =====
            # Calculate interpolation alpha for smooth rendering
            # alpha = how far we are between current and next physics state
            if self.use_interpolation:
                if self.performance_mode == "adaptive":
                    # In adaptive mode, alpha represents the time since the last physics step
                    time_since_physics = time.time() - self.last_physics_time
                    alpha = min(1.0, time_since_physics / self.min_physics_interval)
                else:
                    # In precise mode: use the normal alpha calculation
                    alpha = self.time_accumulator / self.physics_timestep
            else:
                alpha = 1.0
            
            self.current_alpha = alpha
            
            # Clear screen
            if self.screen_mode == "dark":
                self.screen.fill(Display.BLACK)
            else:
                self.screen.fill(Display.WHITE)
            
            # Update and filter expired temporary texts
            self.temp_texts = [text for text in self.temp_texts if text.update()]
            
            # Handle background music
            self.handle_music()
            
            # Render with interpolation
            self.render(alpha)
            
            # Update display and maintain target FPS
            pygame.display.flip()
            clock.tick(self.FPS_TARGET)
        
        # Clean exit
        ActionManager.quit_engine()


# -----------------
# class ActionManager
# -----------------
class ActionManager:
    """
    Static class for handling user actions and input events.
    
    All methods are static as they operate on the global engine instance
    and don't require their own state.
    """
    @staticmethod
    def toggle_pause():
        """Toggle simulation pause state."""
        if engine.is_paused:
            engine.unpause()
        else:
            engine.pause()

    @staticmethod
    def toggle_random_mode():
        """Toggle random velocity mode for new bodies."""
        engine.random_mode = not engine.random_mode

    @staticmethod
    def toggle_reversed_gravity():
        """Toggle reversed gravity mode (repulsion instead of attraction)."""
        engine.reversed_gravity = not engine.reversed_gravity

    @staticmethod
    def toggle_vectors_printed():
        """Toggle display of velocity and force vectors."""
        engine.vectors_printed = not engine.vectors_printed

    @staticmethod
    def quit_engine(text: str = "See you soon!"):
        """
        Quit the simulation and exit the program.
        
        Args:
            text: Exit message (not currently displayed)
        """
        pygame.quit()
        sys.exit(text)

    @staticmethod
    def delete_selected_circle():
        """Delete the currently selected body from the simulation."""
        for circle in circles:
            if circle.is_selected:
                circles.remove(circle)
                break

    @staticmethod
    def handle_mouse_button_down(event: pygame.event):
        """Handle mouse button press with camera transformation."""
        # Don't handle circle creation if in info mode
        if engine.show_help:
            return

        # Right click to pan
        if event.button == 3:  # Right click
            mx, my = pygame.mouse.get_pos()
            engine.camera.start_pan(mx, my)
            return

        # Left click for selection/creation
        if event.button == 1:  # Left click
            engine.circle_collided = None
            engine.can_create_circle = False
            engine.mouse_down = True
            engine.mouse_down_start_time = time.time()
            
            # Convert screen position to world coordinates
            screen_x, screen_y = pygame.mouse.get_pos()
            world_x, world_y = engine.camera.screen_to_world(screen_x, screen_y)
            
            if len(circles) > 0:
                alpha = engine.current_alpha

                # Check collision with bodies (visual positions)
                for circle in circles:
                    # Interpolated visual position (world)
                    visual_world_x = circle.prev_x + (circle.x - circle.prev_x) * alpha
                    visual_world_y = circle.prev_y + (circle.y - circle.prev_y) * alpha

                    # Distance in world coordinates
                    dx = fabs(world_x - visual_world_x)
                    dy = fabs(world_y - visual_world_y)
                    dist = sqrt(dx**2 + dy**2)

                    # Check if click is within the radius
                    if dist <= circle.radius:
                        engine.circle_collided = circle.number
                        for c in circles:
                            if c != circle:
                                c.is_selected = False
                        break

                # Selection handling
                if engine.circle_collided is not None:
                    for circle in circles:
                        if circle.number == engine.circle_collided:
                            circle.switch_selection()
                            break
                elif engine.circle_selected:
                    for circle in circles:
                        circle.is_selected = False
                else:
                    engine.can_create_circle = True

                if engine.can_create_circle:
                    # Create in world coordinates
                    engine.temp_circle = Circle(world_x, world_y, 
                                            engine.default_density, 
                                            mass=engine.minimum_mass)
                    engine.can_create_circle = False
            else:
                # Create in world coordinates
                engine.temp_circle = Circle(world_x, world_y, 
                                        engine.default_density, 
                                        mass=engine.minimum_mass)

        # Handle mouse wheel for zoom.
        if event.button == 4:  # Scroll up
            engine.camera.zoom_at_mouse(zoom_in=True)
        elif event.button == 5:  # Scroll down
            engine.camera.zoom_at_mouse(zoom_in=False)

    @staticmethod
    def handle_mouse_button_up(event: pygame.event):
        """
        Handle mouse button release events.
        
        Finalizes body creation by adding the temporary body to the simulation.
        
        Args:
            event: Pygame mouse button event
        """
        # Don't handle circle creation if in info mode
        if engine.show_help:
            return

        # End pan handling
        if event.button == 3:  # Right click
            engine.camera.end_pan()
            return
        
        # End of body creation
        if event.button == 1:  # Left click
            engine.mouse_down = False
            engine.mouse_down_start_time = None
            if engine.temp_circle is not None:
                circles.append(engine.temp_circle)
                engine.temp_circle = None

    @staticmethod
    def zoom_in():
        """Zoom in centered on screen center."""
        screen_center_x = engine.screen.get_width() // 2
        screen_center_y = engine.screen.get_height() // 2
        
        # Save mouse position
        old_mouse_pos = pygame.mouse.get_pos()
        
        # Simulate mouse in the middle
        pygame.mouse.set_pos(screen_center_x, screen_center_y)
        engine.camera.zoom_at_mouse(zoom_in=True)
        
        # Reload mouse position
        pygame.mouse.set_pos(old_mouse_pos)

    @staticmethod
    def zoom_out():
        """Zoom out centered on screen center."""
        screen_center_x = engine.screen.get_width() // 2
        screen_center_y = engine.screen.get_height() // 2
        
        old_mouse_pos = pygame.mouse.get_pos()
        pygame.mouse.set_pos(screen_center_x, screen_center_y)
        engine.camera.zoom_at_mouse(zoom_in=False)
        pygame.mouse.set_pos(old_mouse_pos)

    @staticmethod
    def reset_camera():
        """Reset camera to default position and zoom."""
        engine.camera.reset()
        TempText("Camera reset",
                1.5,
                (int((engine.screen.get_width() / 2) - (engine.font.size("Camera reset")[0] / 2)),
                engine.info_y - engine.txt_gap - engine.txt_size),
                line=1
                )

    @staticmethod
    def pan_camera(dx, dy):
        """Pan camera by offset."""
        engine.camera.cam_x += dx
        engine.camera.cam_y += dy

    def save_screenshot(path: Optional[str] = None):
        """
        Save a screenshot of the current screen.

        Args:
            path (Optional[str]): file path ending with .png
        """
        if path is None:
            file_name = f"screenshot_{int(time.time())}.png"
            path = f"{engine.screenshots_folder_path}/{file_name}"
            TempText(
                text=f"Screenshot saved as {file_name}",
                duration=3.0,
                dest=(
                    20,
                    engine.screen.get_height() - 2 * (engine.txt_gap + engine.txt_size)
                )
            )

        pygame.image.save(engine.screen, path)


# -----------------
# class Utils
# -----------------
class Utils:
    """
    Utility class providing helper functions for calculations and rendering.
    
    All methods are static utility functions that don't require instance state.
    """
    @staticmethod
    def heaviest() -> Optional[tuple]:
        """
        Find the heaviest body in the simulation.
        
        Returns:
            Tuple of (body_id, mass) if bodies exist, None otherwise
        """
        circles_mass = []

        if len(circles) != 0:
            # Collect all body masses
            for circle in circles:
                circles_mass.append(circle.mass)

            # Find index of maximum mass
            index = circles_mass.index(max(circles_mass))
            circle_id = circles[index].number

            return circle_id, max(circles_mass)
        else:
            return None

    @staticmethod
    def oldest() -> Optional[tuple]:
        """
        Find the oldest body in the simulation.
        
        Returns:
            Tuple of (body_id, age) if bodies exist, None otherwise
        """
        circles_age = []

        if len(circles) != 0:
            # Collect all body ages
            for circle in circles:
                circles_age.append(circle.age)

            # Find index of maximum age
            index = circles_age.index(max(circles_age))
            circle_id = circles[index].number

            return circle_id, max(circles_age)
        else:
            return None

    @staticmethod
    def mass_sum() -> int:
        """
        Calculate total mass of all bodies in the simulation.
        
        Returns:
            Sum of all body masses
        """
        all_mass = 0
        for circle in circles:
            all_mass += circle.mass
        return all_mass

    @staticmethod
    def draw_line(color: tuple[int, int, int] | tuple[int, int, int, int] = (255, 255, 255),
                  start_pos: tuple[float, float] = (0, 0),
                  end_pos: tuple[float, float] = (0, 0),
                  width: int = 1):
        """
        Draw a line on the screen.
        
        Args:
            color: RGB or RGBA color tuple
            start_pos: Starting position (x, y)
            end_pos: Ending position (x, y)
            width: Line width in pixels
        """
        pygame.draw.line(engine.screen, color, start_pos, end_pos, width)
    
    @staticmethod
    def write_screen(text: str = "[text]",
              dest: tuple[int, int] = (0, 0),
              color: tuple[int, int, int] = Color(255, 255, 255),
              line: int = 0) -> Optional[pygame.Rect]:
        """
        Render and display text on the screen.
        
        Args:
            text: Text string to display
            dest: Base position (x, y) for text
            color: RGB color tuple
            line: Line offset for vertical spacing (0 = first line)
        
        Returns:
            Pygame Rect object representing the text area, or None on error
        """
        written = engine.font.render(text, 1, color)
        rect = engine.screen.blit(written, dest=(dest[0], dest[1] + line * (engine.txt_gap + engine.txt_size)))
        return rect

    @staticmethod
    def average(l: list[float] | tuple[float] | set[float]) -> float:
        """
        Calculate arithmetic mean of a sequence of numbers.
        
        Args:
            l: Sequence of numbers (list, tuple, or set)
        
        Returns:
            Average value, or 0 if sequence is empty
        """
        return sum(l) / len(l) if len(l) > 0 else 0


# -----------------
# Starting
# -----------------
if __name__ == '__main__':
    """
    Main entry point for the Gravity Engine simulation.
    
    Initializes pygame, sets up color constants, creates the engine instance,
    and starts the simulation loop.
    """
    # Initialize pygame modules
    pygame.init()

    # Global list of all celestial bodies in the simulation
    circles: list[Circle] = []

    # Create and run the simulation engine
    engine = Engine()
    engine.run()
    