"""
Gravity Engine by Nitr0xis (Nils DONTOT)
Copyright (c) 2026 Nils DONTOT

--- Informations ---
Email: nils.dontot.pro@gmail.com
GitHub account: https://github.com/Nitr0xis/
GitHub repository: https://github.com/Nitr0xis/GravityEngine/
LICENCE: https://creativecommons.org/licenses/by-nc-sa/4.0/, Creative Commons BY-NC-SA 4.0 License
README: https://github.com/Nitr0xis/GravityEngine/blob/main/README.md

Controls:
    - Space -> pause/unpause
    - Mouse wheel (optional) -> create the smallest bodies possible
    - V -> toggle velocity vectors display
    - R -> toggle random_mode
    - G -> toggle reversed gravity
    - Left/Right/Wheel click -> hold to create bodies
                             -> select/deselect a body
    - Delete -> Delete selected body

Parameters:
    All parameters can be edit in Engine.__init__().
    For file paths, consider that you need to write file paths from project's root.
"""


# Standard library imports
import importlib.util  # For dynamic module checking
import os  # For file system operations
import subprocess  # For installing missing modules
import random  # For random number generation
import time  # For time tracking and delays
import sys  # For system-specific parameters and functions

# Import all math functions for convenience (sqrt, sin, cos, atan2, etc.)
from math import *


DISPLAY_API = "pygame"  # pygame or tkinter (actually, only pygame is avaiable)

# Required external modules for the simulation
REQUIRED_MODULES: set[str] = {DISPLAY_API}

# Automatically install missing required modules
for module in REQUIRED_MODULES:
    if importlib.util.find_spec(module) is None:
        # Install module using pip if not found
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Import pygame after ensuring it's installed
import pygame

"""
Todo:
    - add Display class for display between pygame and tkinter
    - update interpolation by adding the choice of the realism (N-compute/s)
    - replace pixel display with screen fractions

Ideas:
    - mass transfer on collision without fusion
    - consider quadtree system for forces

### add rock limit
"""


# ==================================================================================
# ==================================================================================


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


class Core:
    @staticmethod
    def resource_path(relative_path):
        """
        Get absolute path to resource, works for dev and PyInstaller.
        
        This function handles resource path resolution in two scenarios:
        1. Development mode: resolves paths relative to project root
        2. PyInstaller mode: resolves paths from the temporary extraction directory
        
        Args:
            relative_path: Path from project root (e.g., 'assets/font.ttf')

        Returns:
            Absolute path to the resource

        Examples:
            > Core.resource_path('assets/font.ttf')
            'C:/Projects/GravityEngine/assets/font.ttf'  # Dev
            'C:/Users/.../Temp/_MEI123/assets/font.ttf'  # PyInstaller
        """
        try:
            # PyInstaller mode: _MEIPASS is the extracted temp folder
            # This attribute exists when running as a PyInstaller bundle
            base_path = sys._MEIPASS
        except AttributeError:
            # Development mode: go from src/ to project root
            # __file__ = C:/GravityEngine/src/gravity_engine.py
            # dirname once = C:/GravityEngine/src
            # dirname twice = C:/GravityEngine (project root)
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Normalize path separators and join with base path
        return os.path.join(base_path, os.path.normpath(relative_path))


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

    @staticmethod
    def rect():
        pass

    @staticmethod
    def circle():
        pass

    @staticmethod
    def line():
        pass

    @staticmethod
    def write(text: str = "[text]",
              dest: tuple[int, int] = (0, 0),
              color: tuple[int, int, int] = Color(255, 255, 255),
              line: int = 0) -> pygame.Rect | None:
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


class Tester:
    # Units test
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
        test_font = Core.resource_path('assets/font.ttf')
        print(f"Font path: {test_font}")
        print(f"Font exists: {os.path.exists(test_font)}")
        print("=" * 60)


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
            Display.write(self.text, (self.x, self.y + self.line * (engine.txt_gap + engine.txt_size)),
                        self.color)
            return True


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

        # Previous positions for interpolation (rendering with time accumulator)
        # These store the position from the previous physics step
        # Used in draw_interpolated() to smooth rendering between physics updates
        self.prev_x = float(x)
        self.prev_y = float(y)

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

        # Velocity components (pixels per frame)
        self.vx = 0  # Horizontal velocity
        self.vy = 0  # Vertical velocity

        # Speed magnitude (total velocity)
        self.speed = sqrt(self.vx ** 2 + self.vy ** 2) * engine.FPS_TARGET

        # Lifecycle flags
        self.suicide: bool = False  # Flag for removal after fusion

        # Age tracking
        self.is_born = False  # Whether body has been initialized in simulation
        self.birth_time = None  # Timestamp when body was created
        self.age = 0  # Age in simulation time
        self.time_in_pause = 0  # Time spent in paused state

        # UI positioning
        self.info_y: int = 6 * engine.txt_gap + 4 * engine.txt_size  # Y position for info display

        # Vector visualization properties
        self.vector_width = 1  # Line width for velocity vectors
        self.global_speed_vector_scale = 1e6  # in px/m/s
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

    def get_nearest(self) -> tuple[int, float] | None:
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
        Print Global Speed Vector (total velocity vector).
        
        Draws a line from the body's center showing the direction and magnitude
        of its total velocity. The length is scaled by velocity and time factor.
        
        Args:
            in_terminal: If True, also print vector info to console
            alpha: Interpolation factor for smooth rendering (0 to 1)
        """
        # Interpolate position for smooth rendering
        render_x = self.prev_x + (self.x - self.prev_x) * alpha
        render_y = self.prev_y + (self.y - self.prev_y) * alpha

        # Start point is body center
        x1, y1 = render_x, render_y

        # End point calculated from velocity components
        # Scaling factor 17.5 adjusts vector visibility
        x2 = engine.vector_scale * (self.x + self.vx * self.global_speed_vector_scale)
        y2 = engine.vector_scale * (self.y + self.vy * self.global_speed_vector_scale)

        if in_terminal:
            print(f"N{self.number} Start : ({x1}; {y1}); End : ({x2}; {y2})")

        # Draw the velocity vector in red
        Utils.draw_line(self.GSV_color, (x1, y1), (x2, y2), self.vector_width)
        
        # Optionally draw cardinal components (X and Y separately)
        if engine.cardinal_vectors:
            self.print_cardinal_speed_vectors()

    def print_force_vector(self, in_terminal: bool = False, alpha: float = 1.0):
        """
        Print the force vector (net gravitational force).
        
        Draws a line showing the direction and magnitude of the net force
        acting on the body from all other bodies.
        
        Args:
            in_terminal: If True, also print vector info to console
            alpha: Interpolation factor for smooth rendering (0 to 1)
        """
        # Interpolate position for smooth rendering
        render_x = self.prev_x + (self.x - self.prev_x) * alpha
        render_y = self.prev_y + (self.y - self.prev_y) * alpha

        # Calculate force magnitude for scaling
        force_magnitude = sqrt(self.force[0] ** 2 + self.force[1] ** 2)
        
        # Avoid division by zero
        if force_magnitude == 0:
            return  # No force, no vector to draw
        
        # Calculate unit vector (direction)
        unit_x = self.force[0] / force_magnitude
        unit_y = self.force[1] / force_magnitude
        
        # Scale the vector for visibility
        # Use logarithmic scaling for very large/small forces
        # This compresses the range while preserving direction
        if force_magnitude > 0:
            # Logarithmic scaling: log10(force) gives better visibility
            # Add 1 to avoid log(0), multiply by scale factors
            visual_length = log10(force_magnitude + 1) * engine.vector_scale * self.force_vector_scale
        else:
            visual_length = 0
        
        # Calculate end point
        vector_x = unit_x * visual_length
        vector_y = unit_y * visual_length
        end_coordinates = (render_x + vector_x, render_y + vector_y)

        if in_terminal:
            print(f"N{self.number} Force: {force_magnitude:.2e} N, "
                f"Start: ({render_x:.1f}; {render_y:.1f}); End: {end_coordinates}")
        
        # Draw force vector in special blue color
        Utils.draw_line(Display.SP_BLUE, (render_x, render_y), end_coordinates)

    def print_cardinal_speed_vectors(self, in_terminal: bool = False, alpha: float = 1.0):
        """
        Print Cardinal Speed Vectors (X and Y components separately).
        
        Draws two lines showing horizontal (X) and vertical (Y) velocity
        components independently. X component in green, Y component in yellow.
        
        Args:
            in_terminal: If True, also print vector info to console
            alpha: Interpolation factor for smooth rendering (0 to 1)
        """
        # Interpolate position for smooth rendering
        render_x = self.prev_x + (self.x - self.prev_x) * alpha
        render_y = self.prev_y + (self.y - self.prev_y) * alpha

        # Vector's beginning
        x1 = render_x
        y1 = render_y
        
        # Vector's end
        x2 = x1 + self.vx * self.global_speed_vector_scale * engine.vector_scale  # Scaled for visibility        
        y2 = y1 + self.vy * self.global_speed_vector_scale * engine.vector_scale  # Scaled for visibility

        if in_terminal:
            print(f"N{self.number} Start x : ({x1}; {self.y}); End x : ({x2}; {self.y}) " \
                  f"Start y : ({y1}; {self.x}); End y : ({y2}; {self.x})")

        # Draw X component (green horizontal line)
        Utils.draw_line(self.CSV_x_color, (x1, self.y), (x2, self.y), self.vector_width)
        # Draw Y component (yellow vertical line)
        Utils.draw_line(self.CSV_y_color, (self.x, y1), (self.x, y2), self.vector_width)

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
        Display.write(text, (20, y - 20), Display.BLUE, 1)

        # Age display (converted from simulation time to years)
        # 31,557,600 = seconds in a year
        age_years = self.age * engine.time_acceleration / 31_557_600
        if age_years < 2:
            text = f"Age : {round(age_years * 10) / 10} year"
            Display.write(text, (20, y - 20), Display.BLUE, 2)
        else:
            text = f"Age : {round(age_years * 10) / 10} years"
            Display.write(text, (20, y - 20), Display.BLUE, 2)

        # Mass (in kilograms)
        text = f"Mass : {self.mass:.2e} kg"
        Display.write(text, (20, y - 20), Display.BLUE, 3)

        # Radius (in meters)
        text = f"Radius : {round(self.radius * 10) / 10} m"
        Display.write(text, (20, y - 20), Display.BLUE, 4)

        # Volume (in cubic meters)
        text = f"Volume : {self.volume:.2e} m³"
        Display.write(text, (20, y - 20), Display.BLUE, 5)

        # Density (in kilograms by cubic meters)
        text = f"Density : {self.density:.2e} kg/m³"
        Display.write(text, (20, y - 20), Display.BLUE, 6)

        # Kinetic energy (in joules)
        text = f"Kinetic energy : {self.kinetic_energy():.2e} J"
        Display.write(text, (20, y - 20), Display.BLUE, 8)

        # Net force magnitude (in newtons)
        force_magnitude = sqrt(self.printed_force[0] ** 2 + self.printed_force[1] ** 2)
        text = f"Force applied : {force_magnitude:.2e} N"
        Display.write(text, (20, y - 20), Display.BLUE, 9)

        # Velocity magnitude (in m/s)
        text = f"Velocity : {self.speed:.2e} m/s"
        Display.write(text, (20, y - 20), Display.BLUE, 10)

        # Position coordinates
        text = f"Coordinates : {int(self.x)}; {int(self.y)}"
        Display.write(text, (20, y - 20), Display.BLUE, 11)

        # Nearest body information
        nearest_tuple = self.get_nearest()
        if nearest_tuple is not None:
            text = f"Nearest body : n°{nearest_tuple[0]} -> {round(nearest_tuple[1]):.2e} m"
            Display.write(text, (20, y - 20), Display.BLUE, 12)
        else:
            text = f"Nearest body : None"
            Display.write(text, (20, y - 20), Display.BLUE, 12)

    def reset_force_list(self):
        """Clear the list of gravitational forces from other bodies."""
        self.attract_forces = []

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

        # Apply force to velocity if effective (F = ma, so a = F/m, v += a*dt)
        if effective:
            self.vx += fx / self.mass
            self.vy += fy / self.mass

        return fx, fy

    def update_fusion(self, other):
        """
        Check and perform fusion with another body if applicable.
        
        Fusion occurs when:
        - Fusions are enabled
        - This body is larger or equal mass
        - Bodies are overlapping (distance <= radius)
        
        Args:
            other: The other Circle object to check fusion with
        """
        # Calculate distance between bodies
        dx = other.x - float(self.x)
        dy = other.y - float(self.y)
        distance = float(sqrt((dx ** 2) + (dy ** 2)))

        # Check fusion conditions
        if engine.fusions:
            # Only fuse if this body is larger and bodies are overlapping
            if self.mass >= other.mass and distance <= self.radius:
                self.fusion(other)

    def fusion(self, other):
        """
        Merge two bodies, conserving momentum and mass.
        
        The larger body absorbs the smaller one. Position and velocity
        are calculated using center of mass and momentum conservation.
        
        Args:
            other: The other Circle object to merge with (will be destroyed)
        """
        # Calculate total mass
        total_mass = self.mass + other.mass
        
        # Calculate new position using center of mass formula
        # COM = (m1*r1 + m2*r2) / (m1 + m2)
        self.x = (self.x * self.mass + other.x * other.mass) / total_mass
        self.y = (self.y * self.mass + other.y * other.mass) / total_mass

        # Calculate new velocity using momentum conservation
        # p = m*v, so v_new = (p1 + p2) / (m1 + m2)
        self.vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
        self.vy = (self.vy * self.mass + other.vy * other.mass) / total_mass

        # Update mass and recalculate radius from density
        self.mass = total_mass
        # Recalculate radius from new mass and density
        if self.density > 0:
            volume = self.mass / self.density
            self.radius = ((3 * volume) / (4 * pi)) ** (1 / 3)
        else:
            # Fallback to default calculation if density is invalid
            self.radius = self.mass ** (1 / 3)

        # Mark other body for removal
        other.suicide = True

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
    
    def physics_update(self, dt):
        """
        Physics update with fixed timestep.
        
        This method is called by the time accumulator with a fixed dt,
        ensuring deterministic physics regardless of rendering FPS.
        
        Args:
            dt: Fixed physics timestep (always engine.physics_timestep)
        """
        # Store previous position for interpolation
        self.prev_x = self.x
        self.prev_y = self.y
        
        # Calculate net force from all gravitational interactions
        self.force = [0.0, 0.0]
        for f in self.attract_forces:
            self.force[0] += f[0]
            self.force[1] += f[1]
        
        # Calculate force for display (converted to real-world units)
        self.printed_force = [0.0, 0.0]
        for f in self.attract_forces:
            self.printed_force[0] += f[0] / engine.gravity * engine.G
            self.printed_force[1] += f[1] / engine.gravity * engine.G
        
        # Initialize body on first update
        if not self.is_born and self in circles:
            self.birth_time = engine.net_age()
            
            # Apply random initial velocity if random mode enabled
            if engine.random_mode:
                max_velocity_per_frame = sqrt(2 * engine.random_field / self.mass)  # m/frame
                max_velocity = max_velocity_per_frame * engine.FPS_TARGET  # m/s
                self.vx = random.uniform(-max_velocity, max_velocity)  # m/s
                self.vy = random.uniform(-max_velocity, max_velocity)  # m/s
            
            self.is_born = True
        
        # Update age (time since birth, excluding pause time)
        if self.birth_time is not None:
            self.age = engine.net_age() - self.birth_time
        
        # Update geometric properties based on current radius
        self.surface = 4 * self.radius ** 2 * pi
        self.volume = 4 / 3 * pi * self.radius ** 3
        
        # Deselect if body is removed from simulation
        if self not in circles:
            self.is_selected = False
        
        # Calculate speed magnitude
        self.speed = sqrt(self.vx ** 2 + self.vy ** 2)  # m/s
        
        # Update position based on velocity
        dt_sim = dt * engine.time_acceleration
        
        self.x += self.vx * dt_sim  # m/s × s = m
        self.y += self.vy * dt_sim  # m/s × s = m
        
        # Update position tuple
        self.pos = (self.x, self.y)
    
    def draw_interpolated(self, screen, alpha):
        """
        Draw body with interpolated position for smooth rendering.
        
        Uses linear interpolation between previous and current positions
        to provide smooth visual motion even when physics runs at fixed timestep.
        
        Args:
            screen: Pygame screen surface
            alpha: Interpolation factor (0 = previous state, 1 = current state)
        """
        # Interpolate position between previous and current
        # This makes movement appear smooth even with fixed physics timestep
        render_x = self.prev_x + (self.x - self.prev_x) * alpha
        render_y = self.prev_y + (self.y - self.prev_y) * alpha
        
        # --- SECURITY CHECKS ---
        if not isinstance(render_x, (int, float)):
            if isinstance(render_x, (list, tuple)) and len(render_x) > 0:
                render_x = float(render_x[0])
            else:
                render_x = 0.0
                print(f"WARNING: Circle {self.number} had invalid x coordinate, reset to 0")
        
        if not isinstance(render_y, (int, float)):
            if isinstance(render_y, (list, tuple)) and len(render_y) > 0:
                render_y = float(render_y[0])
            else:
                render_y = 0.0
                print(f"WARNING: Circle {self.number} had invalid y coordinate, reset to 0")
        
        if not isinstance(self.radius, (int, float)):
            if isinstance(self.radius, (list, tuple)) and len(self.radius) > 0:
                self.radius = float(self.radius[0])
            else:
                self.radius = 1.0
                print(f"WARNING: Circle {self.number} had invalid radius, reset to 1")
        # -----------------------
        
        # Calculate visible radius (minimum 1 pixel for visibility)
        visible_radius = max(1, int(self.radius))
        
        # Selection highlighting logic
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
                    pygame.draw.circle(screen, Display.DUCKY_GREEN, (int(render_x), int(render_y)),
                                    visible_radius + 2)
                elif visible_radius <= 20:
                    pygame.draw.circle(screen, Display.DUCKY_GREEN, (int(render_x), int(render_y)),
                                    visible_radius + visible_radius // 4 + 1)
                else:
                    pygame.draw.circle(screen, Display.DUCKY_GREEN, (int(render_x), int(render_y)),
                                    visible_radius + 5)
        
        # Draw shadow/outline for unselected bodies
        if not self.is_selected:
            if visible_radius <= 4:
                pygame.draw.circle(screen, Display.DARK_GREY, (int(render_x), int(render_y)), visible_radius + 1)
            elif visible_radius <= 20:
                pygame.draw.circle(screen, Display.DARK_GREY, (int(render_x), int(render_y)),
                                visible_radius + visible_radius // 5)
            else:
                pygame.draw.circle(screen, Display.DARK_GREY, (int(render_x), int(render_y)), visible_radius + 3)
        
        # Draw the main body circle
        self.rect = pygame.draw.circle(screen, self.color, (int(render_x), int(render_y)), visible_radius)


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

        # ==================== SPLASH SCREEN SETTINGS ====================
        self.splash_screen_font = Core.resource_path('assets/fonts/toruk.ttf')
        self.splash_screen_enabled = True  # Enable/disable splash screen
        self.splash_screen_duration = 3.0  # Duration in seconds (can be adjusted)
        self.author_first_name = "Nils"  # Your first name
        self.author_last_name = "DONTOT"  # Your last name
        self.project_description = "Gravity Engine - A celestial body simulation"  # Project description
        self.project_description = "Gravity Engine - A celestial body simulation"  # Project description
        
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
        
        pygame.display.set_caption(f'Gravity Engine by {self.author_first_name} {self.author_last_name}')

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
        self.time_acceleration = 1e7  # Time acceleration factor
        self.growing_speed = 0.1   # Body growth speed when creating
        
        # ==================== UI SETTINGS ====================
        self.used_font = Core.resource_path('assets/fonts/main_font.ttf')
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

        self.minimum_mass = 1000  # in kg
        
        # Default density for new bodies (mass per unit volume)
        # This determines how large a body will be for a given mass
        self.default_density = 5515  # 1000 <=> 1000 kg/m^3, by default on 5.515 (Earth density)
        
        # ==================== VISUALIZATION SETTINGS ====================
        self.vectors_printed = False
        self.force_vectors = True
        self.cardinal_vectors = False
        self.vectors_in_front = True
        self.vector_scale = 1
        
        # ==================== RANDOM GENERATION SETTINGS ====================
        self.random_mode = False
        
        # Define max random energy in Joules
        max_kinetic_energy_joules = 1e-9  # in J
        # Convert in simulation used units (kg⋅m²/frame²)
        self.random_field = max_kinetic_energy_joules / (self.FPS_TARGET ** 2)

        self.random_environment_number: int = 20
        
        # ==================== AUDIO SETTINGS ====================
        self.musics_folder_path = "assets/musics"  # without ressource_path() because it is a folder
        self.music = False
        self.music_volume = 1
        
        # ==================== SIMULATION STATE ====================
        self.is_paused = False
        self.reversed_gravity = False
        
        # Time tracking
        self.beginning_time = time.time()
        self.time_in_pause = 0
        self.pause_beginning = None
        
        # Performance tracking
        self.temp_FPS = self.FPS_TARGET
        self.frequency = self.FPS_TARGET
        self.latency = None
        self.save_time_1 = 0
        self.save_time_2 = 0
        self.counter = 0
        
        # ==================== BODY MANAGEMENT ====================
        self.circle_number = 0
        self.circle_selected = False
        
        # ==================== INPUT HANDLING ====================
        self.inputs: dict = {}
        self.INPUT_MAP = {}
        self.MOUSEBUTTON_MAP = {}
        
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
        """
        Update accumulated pause time.
        
        Called continuously while paused to track total time spent in pause state.
        This ensures accurate time tracking when calculating simulation age.
        """
        self.time_in_pause += time.time() - self.pause_beginning
        self.pause_beginning = time.time()

    def pause(self):
        """
        Pause the simulation.
        
        Stops physics updates while keeping the display active.
        Records the pause start time for accurate time tracking.
        """
        self.pause_beginning = time.time()
        self.is_paused = True

    def unpause(self):
        """
        Resume the simulation.
        
        Updates time tracking for all bodies and the engine to account for
        the time spent in pause state. This ensures age calculations remain accurate.
        """
        # Update pause time for all bodies
        for circle in circles:
            circle.time_in_pause += time.time() - self.pause_beginning

        # Update engine pause time
        self.time_in_pause += time.time() - self.pause_beginning

        # Clear pause state
        self.pause_beginning = None
        self.is_paused = False

    def brut_age(self) -> float:
        """
        Return total elapsed time since simulation start.
        
        Includes time spent in pause state.
        
        Returns:
            Total elapsed time in seconds
        """
        age = time.time() - self.beginning_time
        return age

    def net_age(self) -> float:
        """
        Return net elapsed time excluding pauses.
        
        This represents the actual simulation time, excluding periods
        when the simulation was paused.
        
        Returns:
            Net elapsed time in seconds (excluding pauses)
        """
        age = self.brut_age() - self.time_in_pause
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
            Display.write(text, (20, y), Display.BLUE, 2)
        else:
            text = f"Heaviest body : None"
            Display.write(text, (20, y), Display.BLUE, 2)

        # Show delete instruction when a body is selected
        if self.circle_selected and len(circles) > 0:
            Display.write(f"Delete : Delete key", (
                int((self.screen.get_width() / 2) - (self.font.size("Delete : Delete key")[0] / 2)),
                y), Display.BLUE, 0)

        # Display reversed gravity status (top right)
        if self.reversed_gravity:
            text = f"Reversed gravity (G) : Enabled"
        else:
            text = f"Reversed gravity (G) : Disabled"
        Display.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Display.BLUE, 0)

        # Display velocity vectors status (top right)
        if self.vectors_printed:
            text = f"Vectors (V) : Enabled"
        else:
            text = f"Vectors (V) : Disabled"
        Display.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Display.BLUE, 1)

        # Display random mode status (top right)
        if self.random_mode:
            text = f"Random mode (R) : Enabled"
        else:
            text = f"Random mode (R) : Disabled"
        Display.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Display.BLUE, 2)

        # Display random environment generation hint (top right)
        text = f"Random environment ({self.random_environment_number} bodies) : P"
        Display.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Display.BLUE, 4)

        # Display time acceleration factor (bottom right)
        text = f"Time factor : ×{self.time_acceleration:.2e}"
        Display.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - 2 * self.txt_size - self.txt_gap), Display.BLUE, 0)

        # Display pause status (bottom right)
        if self.is_paused:
            text = f"Pause (Space) : Enabled"
        else:
            text = f"Pause (Space) : Disabled"
        Display.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - self.txt_size), Display.BLUE, 0)

        # Display body count (top left)
        text = f"Number of bodies : {len(circles)}"
        Display.write(text, (20, y), Display.BLUE, 0)

        # Display total mass (top left)
        text = f"Total mass : {round(Utils.mass_sum()):.2e} kg"
        Display.write(text, (20, y), Display.BLUE, 1)

        # Display oldest body information (top left)
        oldest_tuple = Utils.oldest()
        if oldest_tuple is not None:
            # Convert age to years (31,557,600 seconds per year)
            oldest_age_years = oldest_tuple[1] * engine.time_acceleration / 31_557_600
            if oldest_age_years < 2:
                text = f"Oldest body : n°{oldest_tuple[0]} -> {int(oldest_age_years * 10) / 10} year"
                Display.write(text, (20, y), Display.BLUE, 3)
            else:
                text = f"Oldest body : n°{oldest_tuple[0]} -> {int(oldest_age_years * 10) / 10} years"
                Display.write(text, (20, y), Display.BLUE, 3)
        else:
            text = f"Oldest body : None"
            Display.write(text, (20, y), Display.BLUE, 3)

        # Display simulation age (bottom left)
        sim_age_years = self.net_age() * engine.time_acceleration / 31_557_600
        if sim_age_years < 2:
            text = f"Simulation age : {int(sim_age_years * 10) / 10} year"
            Display.write(text, (20, self.screen.get_height() - 20 - engine.txt_size), Display.BLUE, 0)
        else:
            text = f"Simulation age : {int(sim_age_years * 10) / 10} years"
            Display.write(text, (20, self.screen.get_height() - 20 - engine.txt_size), Display.BLUE, 0)

        # Display FPS (bottom center)
        text = f"FPS : {round(self.temp_FPS)}"
        Display.write(text, (int((self.screen.get_width() / 2) - (self.font.size(text)[0] / 2)),
                          int(self.screen.get_height() - 20 - engine.txt_size)), Display.BLUE, 0)

    def generate_environment(self, count: int = 50):
        """
        Generate a random environment with multiple bodies.
        
        Creates bodies at random positions across the screen with default
        properties. The count parameter is ignored; uses random_environment_number instead.
        
        Args:
            count: Ignored parameter (kept for compatibility)
        """
        # Use configured number of bodies instead of parameter
        count = self.random_environment_number
        for c in range(count):
            # Create body at random position with default mass and density
            new = Circle(x=random.uniform(0, self.screen.get_width()),
                         y=random.uniform(0, self.screen.get_height()),
                         density=self.default_density,
                         mass=1000)
            circles.append(new)

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
                pygame.mixer.music.load(Core.ressource_path(f'{self.musics_folder_path}/music1.mp3'))
                pygame.mixer.music.queue(Core.ressoucre_path(f'{self.musics_folder_path}/music2.mp3'))
                pygame.mixer.music.queue(Core.ressource_path(f'{self.musics_folder_path}/music3.mp3'))
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
            self.temp_circle.draw_interpolated(self.screen, alpha)
        
        # Display UI information
        self.print_global_info(self.info_y)
        for circle in circles:
            if circle.is_selected:
                circle.print_info(circle.info_y)

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

        # Main simulation loop
        while running:
            # ===== TIMING =====
            current_time = time.time()
            frame_time = current_time - self.previous_time
            self.previous_time = current_time
            
            # Update performance metrics (for display)
            self.frequency = 1.0 / frame_time if frame_time > 0 else self.FPS_TARGET
            self.latency = frame_time
            
            # Update FPS display at regular intervals
            if self.counter == 0 or self.counter == int(self.FPS_TARGET / 2):
                self.temp_FPS = self.frequency
            
            # Update frame counter
            if self.counter + 1 >= self.FPS_TARGET:
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
                
                # Increase radius with acceleration
                acceleration_factor = exp(time_held * 0.8)
                radius_increase = self.growing_speed * 100 * frame_time * acceleration_factor
                self.temp_circle.radius += radius_increase
                
                # Recalculate mass from radius and density
                if self.temp_circle.density > 0:
                    volume = (4 / 3) * pi * (self.temp_circle.radius ** 3)
                    self.temp_circle.mass = self.temp_circle.density * volume
                else:
                    self.temp_circle.mass = self.temp_circle.radius ** 3
                
                # Check for collision
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
            physics_steps = 0
            while self.time_accumulator >= self.physics_timestep and not self.is_paused:
                # Run one physics step with fixed dt
                self.physics_step(self.physics_timestep)
                
                # Consume time from accumulator
                self.time_accumulator -= self.physics_timestep
                
                # Safety: limit max steps per frame (prevents spiral of death)
                physics_steps += 1
                if physics_steps >= 10:
                    self.time_accumulator = 0
                    break
            
            # Handle pause time tracking
            if self.is_paused:
                self.refresh_pause()
            
            # ===== RENDERING =====
            # Calculate interpolation alpha for smooth rendering
            # alpha = how far we are between current and next physics state
            alpha = self.time_accumulator / self.physics_timestep
            
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
        """
        Handle mouse button press events.
        
        Determines if the click is on an existing body (selection) or
        on empty space (body creation). Creates a temporary body if creating.
        
        Args:
            event: Pygame mouse button event
        """
        # Initialize click state
        engine.circle_collided = None
        engine.can_create_circle = False
        engine.mouse_down = True
        engine.mouse_down_start_time = time.time()  # Record when click started
        x, y = pygame.mouse.get_pos()

        if len(circles) > 0:
            # Check if click is on an existing body
            for circle in circles:
                # Calculate distance from click to body center
                dx = fabs(x - circle.x)
                dy = fabs(y - circle.y)
                dist = sqrt(dx ** 2 + dy ** 2)
                # Use visible radius (minimum 1 pixel) for click detection
                visible_radius = max(1, int(circle.radius))
                click_on_circle: bool = dist <= visible_radius

                if click_on_circle:
                    # Click is on a body - prepare for selection
                    engine.circle_collided = circle.number
                    # Deselect all other bodies
                    for c in circles:
                        if c != circle:
                            c.is_selected = False
                        break

            # Handle selection toggle
            if engine.circle_collided is not None:
                # Toggle selection of clicked body
                for circle in circles:
                    if circle.number == engine.circle_collided:
                        circle.switch_selection()
                        break
            elif engine.circle_selected:
                # Click on empty space while body is selected - deselect all
                for circle in circles:
                    circle.is_selected = False
            else:
                # Click on empty space - allow body creation
                engine.can_create_circle = True

            # Create temporary body if allowed
            if engine.can_create_circle:
                engine.temp_circle = Circle(x, y, engine.default_density, mass=engine.minimum_mass)
                engine.can_create_circle = False
        else:
            # No bodies exist - always create new one
            engine.temp_circle = Circle(x, y, engine.default_density, mass=engine.minimum_mass)

    @staticmethod
    def handle_mouse_button_up(event: pygame.event):
        """
        Handle mouse button release events.
        
        Finalizes body creation by adding the temporary body to the simulation.
        
        Args:
            event: Pygame mouse button event
        """
        engine.mouse_down = False
        engine.mouse_down_start_time = None
        # Finalize body creation if temporary body exists
        if engine.temp_circle is not None:
            circles.append(engine.temp_circle)
            engine.temp_circle = None


# -----------------
# class Utils
# -----------------
class Utils:
    """
    Utility class providing helper functions for calculations and rendering.
    
    All methods are static utility functions that don't require instance state.
    """
    @staticmethod
    def heaviest() -> tuple | None:
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
    def oldest() -> tuple | None:
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

    # Minimum debug
    Tester.default_debug()

    # Global list of all celestial bodies in the simulation
    circles: list[Circle] = []

    # Create and run the simulation engine
    engine = Engine()
    engine.run()
    