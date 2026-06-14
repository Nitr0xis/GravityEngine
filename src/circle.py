import state
import pygame
import warnings
import random
from math import *
from typing import Optional
from color import Color, Display
from utils import Utils
try:
    from math import cbrt
except ImportError:
    def cbrt(x: float) -> float:
        if x >= 0:
            return x ** (1.0 / 3.0)
        return -((-x) ** (1.0 / 3.0))


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
        state.engine.circle_number += 1
        self.number: int = state.engine.circle_number

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
        if state.engine.screen_mode == "dark":
            self.color = Display.WHITE
        elif state.engine.screen_mode == "light":
            self.color = Display.BLACK

        # Selection state
        self.is_selected = False
        if not self in state.circles:
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
        self.info_y: int = 6 * state.engine.txt_gap + 4 * state.engine.txt_size  # Y position for info display

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
        for other in state.circles:
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
        istate = self.get_interpolated_state(alpha)
        
        world_x = istate['x']
        world_y = istate['y']
        render_vx = istate['vx']  # <- Interpolated Speed
        render_vy = istate['vy']  # <- Interpolated Speed
        
        # ===== CONVERT TO SCREEN COORDINATES =====
        screen_x1, screen_y1 = state.engine.camera.world_to_screen(world_x, world_y)
        
        # Calculer la position de fin du vecteur dans le monde
        world_x2 = world_x + render_vx * self.global_speed_vector_scale
        world_y2 = world_y + render_vy * self.global_speed_vector_scale

        # Convert to screen coordinates
        screen_x2, screen_y2 = state.engine.camera.world_to_screen(world_x2, world_y2)

        if in_terminal:
            speed_magnitude = sqrt(render_vx ** 2 + render_vy ** 2)
            print(f"N{self.number} Vector at alpha={alpha:.3f}:")
            print(f"  World position: ({world_x:.1f}, {world_y:.1f})")
            print(f"  Screen position: ({screen_x1:.1f}, {screen_y1:.1f})")
            print(f"  Velocity: ({render_vx:.2f}, {render_vy:.2f}) m/s")

        # ===== DRAW VELOCITY VECTOR =====
        Utils.draw_line(self.GSV_color, (screen_x1, screen_y1), (screen_x2, screen_y2), self.vector_width)

        if state.engine.cardinal_vectors:
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
        istate = self.get_interpolated_state(alpha)
        
        world_x = istate['x']
        world_y = istate['y']
        render_fx = istate['fx']  # <- Interpolated Force
        render_fy = istate['fy']  # <- Interpolated Force

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
        visual_length = log10(force_magnitude + 1) * state.engine.vector_scale * self.force_vector_scale
        
        # ===== CALCULATE END POINT IN WORLD COORDINATES =====
        vector_x = unit_x * visual_length
        vector_y = unit_y * visual_length
        world_end_x = world_x + vector_x
        world_end_y = world_y + vector_y
        
        # ===== CONVERT TO SCREEN COORDINATES =====
        screen_x1, screen_y1 = state.engine.camera.world_to_screen(world_x, world_y)
        screen_x2, screen_y2 = state.engine.camera.world_to_screen(world_end_x, world_end_y)

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
        istate = self.get_interpolated_state(alpha)
        
        world_x = istate['x']
        world_y = istate['y']
        render_vx = istate['vx']  # <- Interpolated X Speed
        render_vy = istate['vy']  # <- Interpolated Y Speed

        # ===== CALCULATE VECTOR ENDPOINTS IN WORLD COORDINATES =====
        # X component (horizontal)
        world_x1 = world_x
        world_x2 = world_x + render_vx * self.global_speed_vector_scale
        
        # Y component (vertical)
        world_y1 = world_y
        world_y2 = world_y + render_vy * self.global_speed_vector_scale
        
        # ===== CONVERT TO SCREEN COORDINATES =====
        # For X component (horizontal line)
        screen_x1, screen_y1 = state.engine.camera.world_to_screen(world_x1, world_y)
        screen_x2, screen_y2 = state.engine.camera.world_to_screen(world_x2, world_y)
        
        # For Y component (vertical line)
        screen_x3, screen_y3 = state.engine.camera.world_to_screen(world_x, world_y1)
        screen_x4, screen_y4 = state.engine.camera.world_to_screen(world_x, world_y2)

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
        pygame.draw.rect(state.engine.screen, Display.BLUE, (20, y, 340, 5))

        # Body ID
        text = f"ID : {self.number}"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 1)

        # Age display (converted from simulation time to years)
        # 31,557,600 = seconds in a year
        age_years = self.age * state.engine.time_acceleration / 31_557_600
        if age_years < 2:
            text = f"Age : {round(age_years * 1000) / 1000} Earth year"
            Utils.write_screen(text, (20, y - 20), Display.BLUE, 2)
        else:
            text = f"Age : {round(age_years * 1000) / 1000} Earth years"
            Utils.write_screen(text, (20, y - 20), Display.BLUE, 2)

        # Mass (in kilograms)
        text = f"Mass : {self.mass:.2e} kg ({self.mass / 5.972e24:.2e} EM)"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 3)

        # Radius (in meters)
        text = f"Radius : {self.radius:.3e} m"
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
        text = f"Coordinates : {int(self.x) / 1000}; {int(self.y) / 1000}"
        Utils.write_screen(text, (20, y - 20), Display.BLUE, 11)

        # Nearest body information
        nearest_tuple = self.get_nearest()
        if nearest_tuple is not None:
            text = f"Nearest body : n°{nearest_tuple[0]} → {round(nearest_tuple[1]):.2e} m"
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
        istate = {
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
        self._interpolated_cache = istate
        
        return istate

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
        force = state.engine.gravity * ((self.mass * other.mass) / (distance ** 2))
        
        # Calculate angle from self to other
        angle = atan2(dy, dx)

        # Decompose force into x and y components
        fx = cos(angle) * force
        fy = sin(angle) * force

        # Apply reversed gravity if enabled (repulsion instead of attraction)
        if state.engine.reversed_gravity:
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

        dt_sim = dt * state.engine.time_acceleration
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
            self.printed_force[0] += f[0] / state.engine.gravity * state.engine.G
            self.printed_force[1] += f[1] / state.engine.gravity * state.engine.G
        
        # ===== INITIALIZATION =====
        # Initialize body on first update
        if not self.is_born and self in state.circles:
            self.birth_time = state.engine.net_simulation_time()
            
            # Apply random initial velocity if random mode enabled
            if state.engine.random_mode:
                # Total energy = energy per kg × mass
                total_energy = state.engine.random_energy_per_kg * self.mass

                # Maximum velocity based on E = 0.5 * m * v²
                max_velocity_per_frame = sqrt(2 * total_energy / self.mass)
                max_velocity = max_velocity_per_frame * state.engine.FPS_TARGET
                
                self.vx = random.uniform(-max_velocity, max_velocity)
                self.vy = random.uniform(-max_velocity, max_velocity)
            
            self.is_born = True
        
        # Update age (time since birth, excluding pause time)
        if self.birth_time is not None:
            self.age = state.engine.net_simulation_time() - self.birth_time
        
        # ===== UPDATE GEOMETRIC PROPERTIES =====
        self.surface = 4 * self.radius ** 2 * pi
        self.volume = 4 / 3 * pi * self.radius ** 3
        
        # Deselect if body is removed from simulation
        if self not in state.circles:
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
        istate = self.get_interpolated_state(alpha)
        
        world_x = istate['x']
        world_y = istate['y']
        if interpolate_radius:
            world_radius = istate['radius']
        
        # ===== CONVERT WORLD → SCREEN =====
        screen_x, screen_y = state.engine.camera.world_to_screen(world_x, world_y)
        
        # ===== CALCULATE VISIBLE RADIUS =====
        # Apply camera scale to radius
        if interpolate_radius:
            screen_radius = world_radius * state.engine.camera.scale
        else:
            screen_radius = self.radius * state.engine.camera.scale
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
                if state.engine.screen_mode == "dark":
                    self.color = Display.WHITE
                elif state.engine.screen_mode == "light":
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

    def _will_collide_continuous(self, other, dt_sim: float) -> bool:
        """
        Continuous collision detection (CCD) over one time step.

        Approximations:
        - Relative velocity is assumed constant during the step.
        - Radius is assumed constant during the step.
        """
        # Relative position at the start of the step
        dx = other.x - self.x
        dy = other.y - self.y

        # Collision radius (sum of radii)
        R = self.radius + other.radius

        # If already overlapping, we're colliding
        if dx * dx + dy * dy <= R * R:
            return True

        # Relative displacement over dt_sim
        dvx = (other.vx - self.vx) * dt_sim
        dvy = (other.vy - self.vy) * dt_sim

        # Quadratic in parameter t ∈ [0,1]: |p + v t| = R
        a = dvx * dvx + dvy * dvy
        if a < 1e-20:
            # No meaningful relative motion
            return False

        b = 2.0 * (dx * dvx + dy * dvy)
        c = dx * dx + dy * dy - R * R

        disc = b * b - 4.0 * a * c
        if disc < 0.0:
            return False

        sqrt_disc = sqrt(disc)
        t1 = (-b - sqrt_disc) / (2.0 * a)
        t2 = (-b + sqrt_disc) / (2.0 * a)

        # Collision si une des racines tombe dans [0,1]
        return (0.0 <= t1 <= 1.0) or (0.0 <= t2 <= 1.0)

    def update_fusion(self, other, dt_sim: float):
        """
        Check and perform fusion with double verification.

        Checks TWO conditions:
        1. Visual collision detected (interpolated positions)
        2. Physical collision confirmed (real positions)
        """
        if not state.engine.fusions:
            return

        if self.mass < other.mass:
            return  # Only the heavier body can absorb

        # ===== PHYSICAL VERIFICATION (real positions + CCD) =====
        dx_real = other.x - self.x
        dy_real = other.y - self.y
        distance_real = sqrt(dx_real**2 + dy_real**2)

        # Instant collision (overlap at current state)
        physical_collision = distance_real <= (self.radius + other.radius)

        # Continuous Collision Detection: did they intersect during this step?
        if not physical_collision:
            physical_collision = self._will_collide_continuous(other, dt_sim)

        # ===== VISUAL VERIFICATION (interpolated positions) =====
        alpha = state.engine.current_alpha

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

        m_self, m_other = self.mass, other.mass
        d_self, d_other = self.density, other.density

        # ===== CALCULATE TOTAL MASS =====
        total_mass = m_self + m_other
        
        # ===== CALCULATE NEW POSITION (CENTER OF MASS) =====
        # COM = (m1*r1 + m2*r2) / (m1 + m2)
        self.x = (self.x * m_self + other.x * m_other) / total_mass
        self.y = (self.y * m_self + other.y * m_other) / total_mass

        # ===== CALCULATE NEW VELOCITY (MOMENTUM CONSERVATION) =====
        # p = m*v, so v_new = (p1 + p2) / (m1 + m2)
        self.vx = (self.vx * m_self + other.vx * m_other) / total_mass
        self.vy = (self.vy * m_self + other.vy * m_other) / total_mass

        # ===== UPDATE MASS =====
        self.mass = total_mass

        # ===== DENSITY (moyenne pondérée par la masse, cohérente avec V = m/ρ) =====
        if d_self > 0 and d_other > 0:
            self.density = (m_self * d_self + m_other * d_other) / total_mass
        elif d_other > 0:
            self.density = d_other
        elif d_self > 0:
            self.density = d_self

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
