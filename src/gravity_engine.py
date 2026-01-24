"""
Gravity Engine by Nils DONTOT
Copyright (c) 2026 Nils DONTOT

--- Informations ---
Email: nils.dontot.pro@gmail.com
GitHub account: https://github.com/NilsDontot/
GitHub repository: https://github.com/NilsDontot/GravityEngine/
LICENCE: https://github.com/NilsDontot/GravityEngine/blob/main/LICENSE, Creative Commons BY-NC-SA 4.0 License
README: https://github.com/NilsDontot/GravityEngine/blob/main/README.md

Controls:
    - Space -> pause/unpause
    - Mouse wheel (optional) -> create the smallest bodies possible
    - V -> toggle velocity vectors display
    - R -> toggle random_mode
    - G -> toggle reversed gravity
    - Left/Right/Wheel click -> hold to create bodies
                             -> select/deselect a body
    - Delete -> Delete selected body
"""


import importlib.util
import os
import subprocess
import random
import time
import math
import sys

from math import *

REQUIRED_MODULES: set[str] = {'pygame'}

for module in REQUIRED_MODULES:
    if importlib.util.find_spec(module) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

import pygame

"""
Todo:
    - finish build process (.bat file)
    - fix units and formulas
    - replace pixel display with screen fractions

Ideas:
    - mass transfer on collision without fusion
    - consider quadtree system for forces

### add rock limit
"""


# ================================================================================================
# ================================================================================================

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)



# -----------------
# class TempText
# -----------------
class TempText:
    def __init__(self, text: str = "", duration: float = 1, dest: tuple[float, float] = (0, 0), line: int = 0,
                 color: tuple[int, int, int] | tuple[int, int, int, int] = (10, 124, 235)):
        """
        Used to display temporary text on the screen.
        It is automatically removed from the list when the duration expires.
        """
        super().__init__()

        engine.temp_texts.append(self)

        self.birth_time = time.time()

        self.text = text
        self.duration = duration

        self.x = dest[0]
        self.y = dest[1] + line * (engine.txt_gap + engine.txt_size)
        self.line = line
        self.color = color

        self.rect = None

    def update(self):
        if time.time() - self.birth_time > self.duration:
            if self in engine.temp_texts:
                engine.temp_texts.remove(self)
            return False
        else:
            Utils.write(self.text, (self.x, self.y + self.line * (engine.txt_gap + engine.txt_size)),
                        self.color)
            return True


# -----------------
# class Circle
# -----------------
class Circle:
    def __init__(self, x, y, radius, mass):
        super().__init__()

        self.pos = None
        self.full_selected_mode = False

        engine.circle_number += 1
        self.number: int = engine.circle_number

        self.x = float(x)
        self.y = float(y)

        self.basic_mass = mass
        self.mass = self.basic_mass

        self.radius = radius
        self.radius = self.mass ** (1 / 3)

        self.surface = 4 * self.radius ** 2 * math.pi
        self.volume = 4 / 3 * math.pi * self.radius ** 3

        self.rect = None

        if engine.screen_mode == "dark":
            self.color = WHITE
        elif engine.screen_mode == "light":
            self.color = BLACK

        self.is_selected = False
        if not self in circles:
            self.is_selected = False

        self.vx = 0
        self.vy = 0

        self.speed = sqrt(self.vx ** 2 + self.vy ** 2) * engine.FPS

        self.suicide: bool = False

        self.is_born = False
        self.birth_time = None
        self.age = 0
        self.time_in_pause = 0

        self.info_y: int = 6 * engine.txt_gap + 4 * engine.txt_size

        self.vector_width = 1
        self.vector_length = engine.vector_length

        self.GSV_color = RED
        self.CSV_x_color = GREEN
        self.CSV_y_color = YELLOW

        self.attract_forces: list[tuple[float, float]] = []
        self.force: list[float] = [0.0, 0.0]
        self.printed_force: list[float] = [0.0, 0.0]

    def draw(self, screen):
        # --- SECURITY ---
        if not isinstance(self.x, (int, float)):
            # If list/tuple, take first element
            if isinstance(self.x, (list, tuple)) and len(self.x) > 0:
                self.x = float(self.x[0])
            else:
                # Otherwise, reset to 0
                self.x = 0.0
                print(f"WARNING: Circle {self.number} had invalid x coordinate, reset to 0")

        if not isinstance(self.y, (int, float)):
            # If list/tuple, take first element
            if isinstance(self.y, (list, tuple)) and len(self.y) > 0:
                self.y = float(self.y[0])
            else:
                # Otherwise, reset to 0
                self.y = 0.0
                print(f"WARNING: Circle {self.number} had invalid y coordinate, reset to 0")

        if not isinstance(self.radius, (int, float)):
            # If list/tuple, take first element
            if isinstance(self.radius, (list, tuple)) and len(self.radius) > 0:
                self.radius = float(self.radius[0])
            else:
                # Otherwise, use default value
                self.radius = 1.0
                print(f"WARNING: Circle {self.number} had invalid radius, reset to 1")
        # ----------------

        #print(self.x, self.y, f"[{type((self.x, self.y))}]")
        if self.full_selected_mode:
            if self.is_selected:
                self.color = DUCKY_GREEN
            else:
                if engine.screen_mode == "dark":
                    self.color = WHITE
                elif engine.screen_mode == "light":
                    self.color = BLACK
        else:
            if self.is_selected:
                if self.radius <= 4:
                    pygame.draw.circle(screen, DUCKY_GREEN, (int(self.x), int(self.y)),
                                       int(self.radius) + 1 + 1)
                elif self.radius <= 20:
                    pygame.draw.circle(screen, DUCKY_GREEN, (int(self.x), int(self.y)),
                                       int(self.radius) + self.radius / 4 + 1)
                else:
                    pygame.draw.circle(screen, DUCKY_GREEN, (int(self.x), int(self.y)),
                                       int(self.radius) + 4 + 1)

        if not self.is_selected:
            if self.radius <= 4:
                pygame.draw.circle(screen, DARK_GREY, (int(self.x), int(self.y)), int(self.radius) + 1)
            elif self.radius <= 20:
                pygame.draw.circle(screen, DARK_GREY, (int(self.x), int(self.y)),
                                   int(self.radius) + self.radius / 5)
            else:
                pygame.draw.circle(screen, DARK_GREY, (int(self.x), int(self.y)), int(self.radius) + 3)

        self.rect = pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

        """
        # Debug tool:
        txt = engine.font.render(f"{self.number}", 1, BLUE)
        engine.screen.blit(txt, (int(self.x), int(self.y)))
        """

    def speed_power(self):
        return 0.5 * self.mass * (self.speed ** 2)

    def switch_selection(self):
        self.is_selected = not self.is_selected

    def get_nearest(self) -> tuple[int, float] | None:
        """
        Find the nearest body.

        :return: (ID of the nearest, distance)
        """
        numbers = []
        distances = []

        for other in circles:
            if other is not self:
                numbers.append(other.number)
                distances.append(sqrt((self.y - other.y) ** 2 + (self.x - other.x) ** 2))

        if len(distances) != 0:
            return numbers[distances.index(min(distances))], min(distances)
        else:
            return None

    def print_GSV(self, in_terminal: bool = False):
        """Print Global Speed Vector."""
        x1 = self.x
        y1 = self.y

        x2 = self.vector_length * (self.x + self.vx * 17.5 * engine.speed)
        y2 = self.vector_length * (self.y + self.vy * 17.5 * engine.speed)

        if in_terminal:
            print(f"N{self.number} Start : ({x1}; {y1}); End : ({x2}; {y2})")

        Utils.draw_line(self.GSV_color, (x1, y1), (x2, y2), self.vector_width)
        if engine.cardinal_vectors:
            self.print_CSV()

    def print_strength_vector(self, in_terminal: bool = False):
        """Print the force vector."""
        force = math.sqrt(self.force[0] ** 2 + self.force[1] ** 2)
        if force != 0:
            coefficient = 5 / force * cbrt(force)
        else:
            coefficient = 0

        vector_x = self.force[0] * coefficient * engine.vector_length * (math.sqrt(engine.speed) / 8)
        vector_y = self.force[1] * coefficient * engine.vector_length * (math.sqrt(engine.speed) / 8)
        end_coordinates = (self.x + vector_x, self.y + vector_y)

        if in_terminal:
            print(f"N{self.number} Start : ({self.x}; {self.y}); End : {end_coordinates}")
        Utils.draw_line(SP_BLUE, (self.x, self.y), end_coordinates)

    def print_CSV(self, in_terminal: bool = False):
        """Print Cardinal Speed Vectors (X and Y components)."""
        x1 = self.x
        x2 = self.x + self.vx * 7

        y1 = self.y
        y2 = self.y + self.vy * 7

        if in_terminal:
            print(f"N{self.number} Start x : ({x1}; {self.y}); End x : ({x2}; {self.y}) " \
                  f"Start y : ({y1}; {self.x}); End y : ({y2}; {self.x})")

        Utils.draw_line(self.CSV_x_color, (x1, self.y), (x2, self.y), self.vector_width)
        Utils.draw_line(self.CSV_y_color, (self.x, y1), (self.x, y2), self.vector_width)

    def print_info(self, y: int):
        """Display detailed body information."""
        pygame.draw.rect(engine.screen, BLUE, (20, y, 340, 5))

        text = f"ID : {self.number}"
        Utils.write(text, (20, y - 20), BLUE, 1)

        # Age display
        if self.age * engine.speed / 31_557_600 < 2:
            text = f"Age : {round(self.age * engine.speed / 31_557_600 * 10) / 10} year"
            Utils.write(text, (20, y - 20), BLUE, 2)
        else:
            text = f"Age : {round(self.age * engine.speed / 31_557_600 * 10) / 10} years"
            Utils.write(text, (20, y - 20), BLUE, 2)

        text = f"Mass : {self.mass:.2e} t"
        Utils.write(text, (20, y - 20), BLUE, 3)

        text = f"Radius : {round(self.radius * 10) / 10} m"
        Utils.write(text, (20, y - 20), BLUE, 4)

        text = f"Volume : {self.volume:.2e} m³"
        Utils.write(text, (20, y - 20), BLUE, 5)

        text = f"Kinetic energy : {self.speed_power():.2e} J"
        Utils.write(text, (20, y - 20), BLUE, 7)

        force_magnitude = math.sqrt(self.printed_force[0] ** 2 + self.printed_force[1] ** 2)
        text = f"Force applied : {force_magnitude:.2e} N"
        Utils.write(text, (20, y - 20), BLUE, 8)

        text = f"Velocity : {self.speed:.2e} m/s"
        Utils.write(text, (20, y - 20), BLUE, 10)

        text = f"Coordinates : {int(self.x)}; {int(self.y)}"
        Utils.write(text, (20, y - 20), BLUE, 11)

        nearest_tuple = self.get_nearest()
        if nearest_tuple is not None:
            text = f"Nearest body : n°{nearest_tuple[0]} -> {round(nearest_tuple[1]):.2e} m"
            Utils.write(text, (20, y - 20), BLUE, 13)
        else:
            text = f"Nearest body : None"
            Utils.write(text, (20, y - 20), BLUE, 13)

    def reset_force_list(self):
        """Clear the forces list."""
        self.attract_forces = []

    def attract(self, other, effective: bool = True) -> tuple[float, float]:
        """Calculate gravitational attraction with another body."""
        dx = other.x - float(self.x)
        dy = other.y - float(self.y)

        distance = float(sqrt((dx ** 2) + (dy ** 2)))

        if distance <= self.radius + other.radius:
            return 0, 0

        force = engine.gravity * ((self.mass * other.mass) / (distance ** 2))
        angle = atan2(dy, dx)

        fx = cos(angle) * force
        fy = sin(angle) * force

        if engine.reversed_gravity:
            fx *= -1
            fy *= -1

        if effective:
            self.vx += fx / self.mass
            self.vy += fy / self.mass

        return fx, fy

    @staticmethod
    def correct_latency(speed: float) -> float:
        """Correct latency based on frame rate."""
        final_speed = speed * 100 * (1 / engine.frequency)
        return final_speed

    def update(self):
        """Update physical state of the body."""
        # Real force
        self.force = [0.0, 0.0]
        for f in self.attract_forces:
            self.force[0] += f[0]
            self.force[1] += f[1]

        if len(self.attract_forces) > 0:
            self.force[0] /= len(self.attract_forces)
            self.force[1] /= len(self.attract_forces)

        # Printed force
        self.printed_force = [0.0, 0.0]
        for f in self.attract_forces:
            self.printed_force[0] += f[0] / engine.gravity * engine.G
            self.printed_force[1] += f[1] / engine.gravity * engine.G

        if len(self.attract_forces) > 0:
            self.printed_force[0] /= len(self.attract_forces)
            self.printed_force[1] /= len(self.attract_forces)

        if not self.is_born and self in circles:
            self.birth_time = engine.net_age()
            # Apply random initial velocity if random mode enabled
            if engine.random_mode:
                self.vx = random.uniform(-1 * math.sqrt(2 * engine.random_field / self.mass),
                                         math.sqrt(2 * engine.random_field / self.mass))
                self.vy = random.uniform(-1 * math.sqrt(2 * engine.random_field / self.mass),
                                         math.sqrt(2 * engine.random_field / self.mass))

            self.is_born = True

        if self.birth_time is not None:
            self.age = engine.net_age() - self.birth_time

        self.surface = 4 * self.radius ** 2 * math.pi
        self.volume = 4 / 3 * math.pi * self.radius ** 3

        if not self in circles:
            self.is_selected = False

        self.speed = sqrt(self.vx ** 2 + self.vy ** 2) * engine.FPS

        self.x += self.correct_latency(self.vx * engine.speed)
        self.y += self.correct_latency(self.vy * engine.speed)

        self.pos = (self.x, self.y)

    def update_fusion(self, other):
        """Check and perform fusion with another body if applicable."""
        dx = other.x - float(self.x)
        dy = other.y - float(self.y)

        distance = float(sqrt((dx ** 2) + (dy ** 2)))

        if engine.fusions:
            if self.mass >= other.mass and distance <= self.radius:
                self.fusion(other)

    def fusion(self, other):
        """Merge two bodies conserving momentum."""
        total_mass = self.mass + other.mass
        self.x = (self.x * self.mass + other.x * other.mass) / total_mass
        self.y = (self.y * self.mass + other.y * other.mass) / total_mass

        self.vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
        self.vy = (self.vy * self.mass + other.vy * other.mass) / total_mass

        self.mass = total_mass
        self.radius = cbrt(self.mass)

        other.suicide = True

    def is_colliding_with(self, other) -> bool:
        """Check collision with another body."""
        dx = other.x - self.x
        dy = other.y - self.y

        distance = sqrt((dx ** 2) + (dy ** 2))

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
            - Mouse wheel (optional) -> create smallest bodies possible
            - V -> toggle velocity vectors
            - R -> toggle random_mode
            - G -> toggle reversed gravity
            - Left/Right/Wheel click -> hold to create bodies
                                    -> select/deselect body
            - Delete -> Delete selected body
        """
        
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
        
        pygame.display.set_caption('Gravity Engine')
        
        # ==================== UI SETTINGS ====================
        self.used_font = resource_path('assets/font.ttf')
        self.txt_size = 30
        self.txt_gap: int = 15
        self.font = pygame.font.Font(self.used_font, self.txt_size)
        self.info_y: int = 20
        
        # Temporary texts
        self.temp_texts: list[TempText] = []
        
        # ==================== PHYSICS SETTINGS ====================
        self.G = 6.6743 * 10 ** -11
        self.default_gravity = self.G
        self.gravity: float = self.default_gravity
        self.fusions = True
        
        # ==================== SIMULATION SETTINGS ====================
        self.FPS = 120
        self.speed = 1_000_000_00  # Time acceleration factor
        self.growing_speed = 0.5   # Body growth speed when creating
        
        # ==================== VISUALIZATION SETTINGS ====================
        self.vectors_printed = False
        self.strength_vectors = True
        self.cardinal_vectors = False
        self.vectors_in_front = True
        self.vector_length = 1
        
        # ==================== RANDOM GENERATION SETTINGS ====================
        self.random_mode = False
        self.random_field = 10 ** -17  # Random velocity energy (kJ)
        self.random_environment_number: int = 20
        
        # ==================== AUDIO SETTINGS ====================
        self.musics_folder_path = resource_path('assets/musics')
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
        self.temp_FPS = self.FPS
        self.frequency = self.FPS
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
        self.can_create_circle = True
        self.circle_collided = False
        self.collision_detected = False
        self.temp_circle: Circle

    def handle_input(self, event: pygame.event.Event = None) -> None:
        if event.type is pygame.KEYDOWN:
            self.inputs[event.key] = True
        elif event.type is pygame.KEYUP:
            self.inputs[event.key] = True

    def refresh_pause(self):
        """Update pause time."""
        self.time_in_pause += time.time() - self.pause_beginning
        self.pause_beginning = time.time()

    def pause(self):
        """Pause the simulation."""
        self.pause_beginning = time.time()
        self.is_paused = True

    def unpause(self):
        """Resume the simulation."""
        for circle in circles:
            circle.time_in_pause += time.time() - self.pause_beginning

        self.time_in_pause += time.time() - self.pause_beginning

        self.pause_beginning = None
        self.is_paused = False

    def brut_age(self) -> float:
        """Return total elapsed time in seconds."""
        age = time.time() - self.beginning_time
        return age

    def net_age(self) -> float:
        """Return net elapsed time (excluding pauses)."""
        age = self.brut_age() - self.time_in_pause
        return age

    def select_circle(self, number: int) -> None:
        """Select a body by its number."""
        for circle in circles:
            if circle.number == number:
                circle.is_selected = True
                self.circle_selected = True
                return None
        TempText(f"Body n°{number} does not exist", 3)

    def print_global_info(self, y):
        """Display global simulation information."""
        heaviest_tuple = Utils.heaviest()
        if heaviest_tuple is not None:
            text = f"Heaviest body : n°{heaviest_tuple[0]} -> {heaviest_tuple[1] / 1000:.2e} t"
            Utils.write(text, (20, y), BLUE, 2)
        else:
            text = f"Heaviest body : None"
            Utils.write(text, (20, y), BLUE, 2)

        text = "(This software includes an FPS correction system)"
        advertisement_printable: bool = heaviest_tuple is not None and self.screen.get_width() - \
                                        self.font.size(f"Reversed gravity (G) : Disabled")[0] - \
                                        self.font.size(f"Heaviest body : n°{heaviest_tuple[0]} -> " \
                                        f"{int(heaviest_tuple[1] * 10) / 10} t")[0] > \
                                        self.font.size(text)[0]
        if advertisement_printable:
            Utils.write(text, (int((self.screen.get_width() / 2) - (self.font.size(text)[0] / 2)), y),
                        BLUE, 0)

        if self.circle_selected and len(circles) > 0:
            Utils.write(f"Delete : Delete key", (
                int((self.screen.get_width() / 2) - (self.font.size("Delete : Delete key")[0] / 2)),
                y + self.txt_size + self.txt_gap), BLUE, 0)

        if self.reversed_gravity:
            text = f"Reversed gravity (G) : Enabled"
        else:
            text = f"Reversed gravity (G) : Disabled"
        Utils.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 0)

        if self.vectors_printed:
            text = f"Vectors (V) : Enabled"
        else:
            text = f"Vectors (V) : Disabled"
        Utils.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 1)

        if self.random_mode:
            text = f"Random mode (R) : Enabled"
        else:
            text = f"Random mode (R) : Disabled"
        Utils.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 2)

        text = f"Random environment ({self.random_environment_number} bodies) : P"
        Utils.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 4)

        text = f"Time factor : ×{self.speed:.2e}"
        Utils.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - 2 * self.txt_size - self.txt_gap), BLUE, 0)

        if self.is_paused:
            text = f"Pause (Space) : Enabled"
        else:
            text = f"Pause (Space) : Disabled"
        Utils.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - self.txt_size), BLUE, 0)

        text = f"Number of bodies : {len(circles)}"
        Utils.write(text, (20, y), BLUE, 0)

        text = f"Total mass : {round(Utils.mass_sum() / 1000) / 1000} kt"
        Utils.write(text, (20, y), BLUE, 1)

        oldest_tuple = Utils.oldest()
        if oldest_tuple is not None:
            oldest_age_years = oldest_tuple[1] * engine.speed / 31_557_600
            if oldest_age_years < 2:
                text = f"Oldest body : n°{oldest_tuple[0]} -> {int(oldest_age_years * 10) / 10} year"
                Utils.write(text, (20, y), BLUE, 3)
            else:
                text = f"Oldest body : n°{oldest_tuple[0]} -> {int(oldest_age_years * 10) / 10} years"
                Utils.write(text, (20, y), BLUE, 3)
        else:
            text = f"Oldest body : None"
            Utils.write(text, (20, y), BLUE, 3)

        sim_age_years = self.net_age() * engine.speed / 31_557_600
        if sim_age_years < 2:
            text = f"Simulation age : {int(sim_age_years * 10) / 10} year"
            Utils.write(text, (20, self.screen.get_height() - 20 - engine.txt_size), BLUE, 0)
        else:
            text = f"Simulation age : {int(sim_age_years * 10) / 10} years"
            Utils.write(text, (20, self.screen.get_height() - 20 - engine.txt_size), BLUE, 0)

        text = f"FPS : {round(self.temp_FPS)}"
        Utils.write(text, (int((self.screen.get_width() / 2) - (self.font.size(text)[0] / 2)),
                          int(self.screen.get_height() - 20 - engine.txt_size)), BLUE, 0)

    def generate_environment(self, count: int = 50):
        """Generate random environment with bodies."""
        count = self.random_environment_number
        for c in range(count):
            new = Circle(x=random.uniform(0, self.screen.get_width()),
                         y=random.uniform(0, self.screen.get_height()),
                         radius=0.1,
                         mass=1)
            circles.append(new)

    def get_frequency(self) -> float:
        """Return current frame frequency."""
        frequency = 1 / self.get_latency()
        self.save_time_1 = time.time()
        return frequency

    def get_latency(self) -> float:
        """Return latency since last frame."""
        latency = time.time() - self.save_time_2
        self.save_time_2 = time.time()
        return latency

    def handle_music(self, loop: int = 0, start: float = 0, fade_ms: int = 0):
        """Handle background music playback."""
        if not pygame.mixer.music.get_busy() and self.music is True:
            try:
                pygame.mixer.music.load(f'{self.musics_folder_path}/music1.mp3')
                pygame.mixer.music.queue(f'{self.musics_folder_path}/music2.mp3')
                pygame.mixer.music.queue(f'{self.musics_folder_path}/music3.mp3')
            except FileNotFoundError:
                pass
            pygame.mixer.music.play(loop, start, fade_ms)

    def run(self):
        """Launch the main simulation loop."""
        pygame.mixer.music.set_volume(self.music_volume)

        global circles
        circles = []

        self.temp_circle = None
        self.mouse_down = False

        clock = pygame.time.Clock()

        self.circle_selected = False

        self.KEY_MAP = {
            pygame.K_SPACE: ActionManager.toggle_pause,
            pygame.K_v: ActionManager.toggle_vectors_printed,
            pygame.K_r: ActionManager.toggle_random_mode,
            pygame.K_g: ActionManager.toggle_reversed_gravity,
            pygame.K_p: self.generate_environment,
            pygame.K_DELETE: ActionManager.delete_selected_circle,
            pygame.K_ESCAPE: ActionManager.quit_engine,
        }
        self.MOUSEBUTTON_MAP = {
            pygame.MOUSEBUTTONDOWN: ActionManager.handle_mouse_button_down,
            pygame.MOUSEBUTTONUP: ActionManager.handle_mouse_button_up,
        }

        running = True

        # Main loop
        while running:
            if self.screen_mode == "dark":
                self.screen.fill(BLACK)
            elif self.screen_mode == "light":
                self.screen.fill(WHITE)

            # Filter expired texts in one line
            self.temp_texts = [text for text in self.temp_texts if text.update()]

            if self.counter == 0 or self.counter == int(self.FPS / 2):
                self.temp_FPS = self.frequency

            if self.counter + 1 >= self.FPS:
                self.counter = 0
            else:
                self.counter += 1

            self.frequency = self.get_frequency()
            self.latency = self.get_latency()

            for circle in circles:
                if circle.is_selected:
                    self.circle_selected = True
                    for other in circles:
                        if circle != other:
                            other.is_selected = False
                    break
                else:
                    self.circle_selected = False

            self.handle_music()

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

            # Mouse button hold behavior
            if self.mouse_down and self.temp_circle:
                self.temp_circle.radius += self.growing_speed * 100 * (1 / self.frequency)
                self.temp_circle.mass = self.temp_circle.radius ** 3
                self.collision_detected = False
                for circle in circles:
                    if self.temp_circle.is_colliding_with(circle):
                        self.collision_detected = True
                        break

                if self.collision_detected:
                    circles.append(self.temp_circle)
                    self.temp_circle = None
                    self.mouse_down = False

            # Remove suicidal bodies
            for circle in circles:
                if circle.suicide is True:
                    circles.remove(circle)

            if self.is_paused:
                self.refresh_pause()
            else:
                # Calculate gravitational forces
                for circle in circles:
                    for other_circle in circles:
                        if circle != other_circle:
                            circle.attract_forces.append(circle.attract(other_circle))
                            circle.update_fusion(other_circle)

                # Update bodies
                for circle in circles:
                    circle.update()

            # Render
            if self.vectors_in_front:
                for circle in circles:
                    circle.draw(self.screen)
                if self.vectors_printed:
                    for circle in circles:
                        if self.strength_vectors:
                            circle.print_strength_vector(False)
                        circle.print_GSV(False)
            else:
                if self.vectors_printed:
                    for circle in circles:
                        if self.strength_vectors:
                            circle.print_strength_vector(False)
                        circle.print_GSV(False)
                for circle in circles:
                    circle.draw(self.screen)

            if self.temp_circle:
                self.temp_circle.draw(self.screen)

            self.print_global_info(self.info_y)
            for circle in circles:
                if circle.is_selected:
                    circle.print_info(circle.info_y)
                circle.reset_force_list()

            pygame.display.flip()
            clock.tick(self.FPS)

        ActionManager.quit_engine()


# -----------------
# class ActionManager
# -----------------
class ActionManager:
    @staticmethod
    def toggle_pause():
        if engine.is_paused:
            engine.unpause()
        else:
            engine.pause()

    @staticmethod
    def toggle_random_mode():
        engine.random_mode = not engine.random_mode

    @staticmethod
    def toggle_reversed_gravity():
        engine.reversed_gravity = not engine.reversed_gravity

    @staticmethod
    def toggle_vectors_printed():
        engine.vectors_printed = not engine.vectors_printed

    @staticmethod
    def quit_engine(text: str = "See you soon!"):
        pygame.quit()
        sys.exit(text)

    @staticmethod
    def delete_selected_circle():
        for circle in circles:
            if circle.is_selected:
                circles.remove(circle)
                break

    @staticmethod
    def handle_mouse_button_down(event: pygame.event):
        engine.circle_collided = None
        engine.can_create_circle = False
        engine.mouse_down = True
        x, y = pygame.mouse.get_pos()

        if len(circles) > 0:
            for circle in circles:
                dx = fabs(x - circle.x)
                dy = fabs(y - circle.y)
                dist = sqrt(dx ** 2 + dy ** 2)
                click_on_circle: bool = dist <= circle.radius

                if click_on_circle:
                    engine.circle_collided = circle.number
                    for c in circles:
                        if c != circle:
                            c.is_selected = False
                        break

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
                engine.temp_circle = Circle(x, y, 3, 1)
                engine.can_create_circle = False
        else:
            engine.temp_circle = Circle(x, y, 3, 1)

    @staticmethod
    def handle_mouse_button_up(event: pygame.event):
        engine.mouse_down = False
        if engine.temp_circle is not None:
            circles.append(engine.temp_circle)
            engine.temp_circle = None


# -----------------
# class Utils
# -----------------
class Utils:
    @staticmethod
    def heaviest() -> tuple | None:
        """Find the heaviest body."""
        circles_mass = []

        if len(circles) != 0:
            for circle in circles:
                circles_mass.append(circle.mass)

            index = circles_mass.index(max(circles_mass))
            circle_id = circles[index].number

            return circle_id, max(circles_mass)
        else:
            return None

    @staticmethod
    def oldest() -> tuple | None:
        """Find the oldest body."""
        circles_age = []

        if len(circles) != 0:
            for circle in circles:
                circles_age.append(circle.age)

            index = circles_age.index(max(circles_age))
            circle_id = circles[index].number

            return circle_id, max(circles_age)
        else:
            return None

    @staticmethod
    def mass_sum() -> int:
        """Return total mass of all bodies."""
        all_mass = 0
        for circle in circles:
            all_mass += circle.mass
        return all_mass

    @staticmethod
    def draw_line(color: tuple[int, int, int] | tuple[int, int, int, int] = (255, 255, 255),
                  start_pos: tuple[float, float] = (0, 0),
                  end_pos: tuple[float, float] = (0, 0),
                  width: int = 1):
        """Draw a line on the screen."""
        pygame.draw.line(engine.screen, color, start_pos, end_pos, width)

    @staticmethod
    def average(l: list[float] | tuple[float] | set[float]) -> float:
        """Calculate arithmetic mean of a sequence."""
        return sum(l) / len(l) if len(l) > 0 else 0

    @staticmethod
    def write(text: str = "[text]",
              dest: tuple[int, int] = (0, 0),
              color: tuple[int, int, int] = (255, 255, 255),
              line: int = 0) -> pygame.Rect | None:
        """Write text to the screen."""
        written = engine.font.render(text, 1, color)
        rect = engine.screen.blit(written, dest=(dest[0], dest[1] + line * (engine.txt_gap + engine.txt_size)))
        return rect


# -----------------
# Starting
# -----------------
if __name__ == '__main__':
    pygame.init()

    # Colors
    WHITE = (255, 255, 255)
    BLUE = (10, 124, 235)
    SP_BLUE = (130, 130, 220)
    BLACK = (0, 0, 0)
    DUCKY_GREEN = (28, 201, 89)
    GREEN = (0, 255, 0)
    YELLOW = (241, 247, 0)
    DARK_GREY = (100, 100, 100)
    RED = (255, 0, 0)

    circles: list[Circle] = []

    engine = Engine()
    engine.run()
