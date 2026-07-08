"""
Gravity Engine 3.8 by Nitr0xis (Nils DONTOT) - Real-time N-body Gravity Simulator
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
    B : Toggle gravitational lensing grid (background)

CONFIGURATION (in state.engine.__init__()) (Main parameters):
    time_acceleration     : Simulation speed (default: 4e6)
    FPS_TARGET            : Rendering FPS (default: 120)
    default_density       : Body density kg/m³ (default: 5514)
    fusions               : Enable/disable body fusion (default: True)

PHYSICS:
    Newtonian gravity (F = G×m₁×m₂/r²), momentum conservation,
    fixed timestep, visual collision detection
"""


# Standard library imports
import importlib.util  # For dynamic module checking
import os  # For file system operations
import subprocess  # For installing missing modules
import random  # For random number generation
import time  # For time tracking and delays
import sys  # For system-specific parameters and functions
from typing import Optional  # For args typing
import warnings  # Used to display warning messages about deprecated features or potential issues

from math import *


# Required external modules for the simulation
EXTERNAL_REQUIRED_MODULES: set[str] = {"pygame", "matplotlib"}

for module in EXTERNAL_REQUIRED_MODULES:
    if importlib.util.find_spec(module) is None:
        print(f"Installing module {module}...")
        # Install module using pip if not found
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        except subprocess.CalledProcessError:
            warnings.warn(f"The pre-installation of the module {module} has failed.")
            warnings.warn(
                f"Module '{module}' is not installed. Install with: {sys.executable} -m pip install {module}",
                stacklevel=1,
            )

# Import modules after ensuring it's installed
try:
    import pygame
except ImportError:
    raise ImportError("\"pygame\" module is not installed")

# For future ideas:
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("\"matplotlib\" module is not installed")

# Import my own modules
import state
from logger import Logger
from color import Color, Display
from camera import Camera
from circle import Circle
from temp_text import TempText
from utils import Utils
from action_manager import ActionManager
from config_panel import ConfigPanel
from gravitational_grid import draw_gravitational_grid
from atlas import FileManager
from debugger import Debugger

# Référence globale attendue par Circle, TempText, ActionManager, Utils, etc.
engine: Optional["Engine"] = None

 
"""
Todo:
    - redo the key bindings using the ctrl key
    - update code structure
    - add a focus mode
    - add a "define as referential button"
    - add collision epsilon
    - add a color field which shows the attract field of the selected body
    - consider quadtree system for forces
    - mass transfer on collision without fusion
    - add senarios in json
    - add .csv export method

For my NSI projects:
    - advanced data system with curves (choice between pygame and tkinter) [using matplotlib + tkinter in the same window]

Ideas:
    -=-=-=-=-
"""


# ==================================================================================
# ==================================================================================


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
            dev_data_folder="user_data",
            use_documents=True
        )
        
        # Create necessary folders
        self.screenshots_folder_path = self.fm.create_folder('screenshots')
        self.saves_folder_path = self.fm.create_folder('saves')
        self.logs_folder_path = self.fm.create_folder('logs')
        Logger.setup(self.logs_folder_path)

        # ==================== SPLASH SCREEN SETTINGS ====================
        self.splash_screen_font = self.fm.resource_path('assets/fonts/main_font.ttf')
        self.splash_screen_enabled = True  # Enable/disable splash screen
        self.splash_screen_duration = 3.0  # Duration in seconds (can be adjusted)
        self.author_first_name = "Nils"  # Your first name
        self.author_last_name = "DONTOT"  # Your last name
        self.project_version = "3.8.0"
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

        # ==================== CONFIGURATION PANEL ====================
        self.config_panel: ConfigPanel | None = None  # Will be created on first open

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

        # Grille de fond (lentille gravitationnelle, infinie, sensible à la caméra)
        self.gravitational_grid_enabled: bool = False
        self.grid_lens_amount: float = 3.5  # intensité de la déformation (0 = pas d'effet)
        self.grid_target_spacing_px: float = 72.0  # espacement cible à l'écran (px)
        self.grid_max_lines: int = 64
        self.grid_subdivide_px: float = 96.0  # au-delà, sous-grille 1/5 du pas majeur
        self.grid_lens_softening_world: float = 0.0  # 0 = auto (rayon + fraction de la vue)
        # When enabled, each fixed physics step can be subdivided into
        # additional substeps based on bodies' speeds and radii.
        # This helps avoid fast bodies tunnelling through others.
        self.adaptive_substeps: bool = False
        # Max extra substeps per base step (0 = disabled, 1 = up to 2x, etc.)
        self.adaptive_substeps_max_extra: float = 0.0

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
        self._fps_display_accumulator = 0.0

        # ==================== SIMULATION TIME ====================
        # time tracking
        self.simulation_time = 0.0  # Actual simulation time calculated (in seconds)
        self.simulation_time_in_pause = 0.0  # Wall-clock seconds spent paused (statistics)
        self._pause_wall_clock_start: Optional[float] = None

        # ==================== VISUAL COLLISION HANDLING ====================
        self.skip_prev_update = False  # Flag to prevent updating prev_x/prev_y
        
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

        global engine
        state.engine = self

        Logger.info("Engine initialized")

    # ==================== UI HELPERS ====================
    def notify(self, text: str, duration: float = 2.0, line: int = 0) -> None:
        """
        Display a small temporary message at the bottom of the screen.
        Used by the configuration panel to confirm actions.
        """
        y = self.screen.get_height() - (line + 2) * (self.txt_gap + self.txt_size)
        TempText(
            text=text,
            duration=duration,
            dest=(20, y)
        )
        Logger.info(f"Temporary message displayed: {text}")

    # ==================== CAMERA PROPERTIES (for UI) ====================
    @property
    def camera_zoom(self) -> float:
        """
        Zoom de la caméra exposé au panneau de configuration.
        
        Utilise directement le facteur de zoom interne de la caméra.
        """
        return self.camera.scale

    @camera_zoom.setter
    def camera_zoom(self, value: float) -> None:
        """
        Update the camera zoom from the UI.
        
        Value is automatically clamped between min_scale and max_scale.
        """
        if not hasattr(self, "camera"):
            return
        # Clamp to the camera allowed range
        value = max(self.camera.min_scale, min(value, self.camera.max_scale))
        self.camera.scale = value

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

    def pause(self):
        """
        Pause the simulation.
        
        Stops physics updates while keeping the display active.
        Records the pause start time for accurate time tracking.
        """
        if not self.is_paused:
            self._pause_wall_clock_start = time.time()
        self.is_paused = True

    def unpause(self):
        """
        Resume the simulation.
        
        Updates time tracking for all bodies and the engine to account for
        the time spent in pause state. This ensures age calculations remain accurate.
        """
        if self._pause_wall_clock_start is not None:
            self.simulation_time_in_pause += time.time() - self._pause_wall_clock_start
            self._pause_wall_clock_start = None
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
        for circle in state.circles:
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
            text = f"Heaviest body : n°{heaviest_tuple[0]} → {heaviest_tuple[1]:.2e} kg"
            Utils.write_screen(text, (20, y), Display.BLUE, 2)
        else:
            text = f"Heaviest body : None"
            Utils.write_screen(text, (20, y), Display.BLUE, 2)

        # Show delete instruction when a body is selected
        if self.circle_selected and len(state.circles) > 0:
            Utils.write_screen(f"Delete : Delete key", (
                int((self.screen.get_width() / 2) - (self.font.size("Delete : Delete key")[0] / 2)),
                y), Display.BLUE, 0)

        text = "Hold H or I to display the help box"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Color(150, 0, 0), 0)

        text = "Press C to show the config menu"
        Utils.write_screen(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), Color(150, 0, 0), 1)

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
        text = f"Number of bodies : {len(state.circles)}"
        Utils.write_screen(text, (20, y), Display.BLUE, 0)

        # Display total mass (top left)
        text = f"Total mass : {Utils.mass_sum():.2e} kg ({Utils.mass_sum() / 5.972e24:.2e} EM)"
        Utils.write_screen(text, (20, y), Display.BLUE, 1)

        # Display oldest body information (top left)
        oldest_tuple = Utils.oldest()
        if oldest_tuple is not None:
            # Convert age to years (31,557,600 seconds per year)
            oldest_age_years = oldest_tuple[1] * state.engine.time_acceleration / 31_557_600
            if oldest_age_years < 2:
                text = f"Oldest body : n°{oldest_tuple[0]} → {int(oldest_age_years * 1000) / 1000} Earth year"
                Utils.write_screen(text, (20, y), Display.BLUE, 3)
            else:
                text = f"Oldest body : n°{oldest_tuple[0]} → {int(oldest_age_years * 1000) / 1000} Earth years"
                Utils.write_screen(text, (20, y), Display.BLUE, 3)
        else:
            text = f"Oldest body : None"
            Utils.write_screen(text, (20, y), Display.BLUE, 3)

        # Display simulation age (bottom left)
        sim_age_years = self.net_simulation_time() * state.engine.time_acceleration / 31_557_600
        if sim_age_years < 2:
            text = f"Simulation age : {int(sim_age_years * 1000) / 1000} Earth year"
            Utils.write_screen(text, (20, self.screen.get_height() - 20 - state.engine.txt_size), Display.BLUE, 0)
        else:
            text = f"Simulation age : {int(sim_age_years * 1000) / 1000} Earth years"
            Utils.write_screen(text, (20, self.screen.get_height() - 20 - state.engine.txt_size), Display.BLUE, 0)

        # Display FPS (bottom center)
        text = f"FPS : {round(self.displayed_FPS)}"
        Utils.write_screen(text, (int((self.screen.get_width() / 2) - (self.font.size(text)[0] / 2)),
                          int(self.screen.get_height() - 20 - state.engine.txt_size)), Display.BLUE, 0)

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
                    ("V", "Toggle vectors display (red: velocity vectors, blue: force vectors)"),
                    ("B", "Toggle gravitational lensing grid (infinite background)"),
                    ("R", "Toggle random velocity mode (mass-proportional)"),
                    ("G", "Toggle reversed gravity (repulsion)"),
                    ("P", f"Generate random environment ({self.random_environment_number} bodies, zoom-adaptive)"),
                    ("S", "Take a screenshot"), ("", f"Saved in {self.screenshots_folder_path}"),
                    ("Delete", "Delete selected body"),
                    ("H / I", "Toggle this help overlay"),
                    ("C", "Toggle the config panel"),
                    ("Escape/Alt+F4", "Exit program"),
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
            state.circles.append(new)
        
        # ===== USER FEEDBACK =====
        if temptext:
            TempText(
                f"Generated {count} bodies (zoom: {zoom_factor:.2e}x)",
                2.0,
                (int((self.screen.get_width() / 2) - 200),
                self.info_y - self.txt_gap - self.txt_size),
                line=2
            )
        Logger.info(f"Generated {count} bodies (zoom: {zoom_factor:.2e}x)")

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
                mus_dir = self.fm.resource_path("assets/musics")
                m1 = os.path.join(mus_dir, "music1.mp3")
                m2 = os.path.join(mus_dir, "music2.mp3")
                m3 = os.path.join(mus_dir, "music3.mp3")
                pygame.mixer.music.load(m1)
                pygame.mixer.music.queue(m2)
                pygame.mixer.music.queue(m3)
                pygame.mixer.music.play(loop, start, fade_ms)
            except (FileNotFoundError, OSError, pygame.error, AttributeError):
                pass
    
    ### A passer en GO
    def physics_step(self, dt):
        """
        Execute one physics step with fixed timestep.
        
        This ensures deterministic physics regardless of rendering FPS.
        Always called with dt = self.physics_timestep (1/120 (state.engine.FPS_TARGET) s).
        
        Args:
            dt: Fixed timestep duration (always self.physics_timestep)
        """
        # Simulated duration (including time acceleration factor)
        dt_sim = dt * self.time_acceleration
        # Remove bodies marked for deletion (after fusion)
        circles_to_remove = [circle for circle in state.circles if circle.suicide]
        for circle in circles_to_remove:
            state.circles.remove(circle)
        
        # Calculate gravitational forces between all body pairs
        for circle in state.circles:
            circle.attract_forces.clear()  # Reset force list
            for other_circle in state.circles:
                if circle != other_circle:
                    # Calculate and store attraction force
                    circle.attract_forces.append(circle.attract(other_circle))
                    # Check for fusion conditions (with CCD on the current step)
                    circle.update_fusion(other_circle, dt_sim)
        
        # Update all bodies (position, velocity, age, etc.)
        for circle in state.circles:
            circle.physics_update(dt)

        # IMPORTANT: Increment simulation time
        self.simulation_time += dt

    def physics_step_with_substeps(self, dt: float) -> None:
        """
        Execute a physics step, optionally subdivided into adaptive substeps.

        - If self.adaptive_substeps is False or max extra is 0,
          a single physics_step(dt) is executed.
        - Otherwise, we estimate how many substeps are needed to
          limit displacement relative to radius.
        """
        if not self.adaptive_substeps or self.adaptive_substeps_max_extra <= 0.0:
            self.physics_step(dt)
            return

        # Estimate the worst displacement / radius ratio
        max_ratio = 0.0
        if len(state.circles) > 0:
            for c in state.circles:
                if c.radius <= 0:
                    continue
                # Speed already computed (m/s) or recomputed if missing
                speed = getattr(c, "speed", sqrt(c.vx ** 2 + c.vy ** 2))
                # Displacement over the simulated step
                disp = speed * dt * self.time_acceleration
                ratio = disp / c.radius if c.radius > 0 else 0.0
                if ratio > max_ratio:
                    max_ratio = ratio

        # Threshold: target max displacement ≈ 0.5 radius per substep
        threshold = 0.5
        if max_ratio <= 0.0:
            substeps = 1
        else:
            required = ceil(max_ratio / threshold)
            max_allowed = 1 + int(self.adaptive_substeps_max_extra)
            substeps = max(1, min(required, max_allowed))

        sub_dt = dt / substeps
        for _ in range(substeps):
            self.physics_step(sub_dt)
    
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
            for circle in state.circles:
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
            for circle in state.circles:
                if hasattr(circle, '_visual_x'):
                    circle.prev_x = circle._visual_x
                    circle.prev_y = circle._visual_y
                    # Clean up
                    delattr(circle, '_visual_x')
                    delattr(circle, '_visual_y')
        
            # STEP 4: Reset alpha to 0 (start again from the saved visual position)
            alpha = 0

        draw_gravitational_grid(self.screen, self, alpha, state.circles)

        # Render vectors if enabled
        if self.vectors_in_front:
            # Bodies first, then vectors on top
            for circle in state.circles:
                circle.draw_interpolated(self.screen, alpha)
            if self.vectors_printed:
                for circle in state.circles:
                    circle.print_global_speed_vector(False, alpha)
                    if self.force_vectors:
                        circle.print_force_vector(False, alpha)
                    
        else:
            # Vectors first, then bodies on top
            if self.vectors_printed:
                for circle in state.circles:
                    circle.print_global_speed_vector(False ,alpha)
                    if self.force_vectors:
                        circle.print_force_vector(False, alpha)
                    
            for circle in state.circles:
                circle.draw_interpolated(self.screen, alpha)
        
        # Draw temporary body being created
        if self.temp_circle:
            self.temp_circle.draw_interpolated(self.screen, alpha, interpolate_radius=False)
        
        # Display UI information
        if not self.show_help:
            self.print_global_info(self.info_y)
            for circle in state.circles:
                if circle.is_selected:
                    circle.print_info(circle.info_y)
        else:
            self.show_help_overlay()

    def _check_visual_collisions(self, alpha):
        """Check if any bodies collide at interpolated positions."""
        for i, circle in enumerate(state.circles):
            if circle.suicide:
                continue
            
            # Position interpolée
            x1 = circle.prev_x + (circle.x - circle.prev_x) * alpha
            y1 = circle.prev_y + (circle.y - circle.prev_y) * alpha
            
            for other in state.circles[i+1:]:
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

        Logger.info("Showing splash screen")
        
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
                    ActionManager.quit_engine()
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
        Debugger.default_debug()

        # Show splash screen at startup
        self.show_splash_screen()
        
        # Initialize music volume
        pygame.mixer.music.set_volume(self.music_volume)

        # Initialize global body list
        state.circles.clear()

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
            pygame.K_b: ActionManager.toggle_gravitational_grid,
            pygame.K_r: ActionManager.toggle_random_mode,
            pygame.K_g: ActionManager.toggle_reversed_gravity,
            pygame.K_p: self.generate_environment,
            pygame.K_DELETE: ActionManager.delete_selected_circle,
            pygame.K_ESCAPE: ActionManager.quit_engine,
            # ===== CAMERA =====
            pygame.K_a: ActionManager.zoom_in,      # A to zoom in
            pygame.K_e: ActionManager.zoom_out,    # E to zoom out
            pygame.K_t: ActionManager.reset_camera,    # T to reset
            # ===== CONFIGURATION PANEL =====
            pygame.K_c: lambda: ActionManager.open_config_panel(),
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

        self.beginning_time = time.time()

        running = True

        # Initialize time tracking
        self.previous_time = time.time()
        self.time_accumulator = 0.0

        Logger.info("Main loop initialized")

        # ======== MAIN LOOP ========
        while running:
            # ===== TIMING =====
            current_time = time.time()
            frame_time = current_time - self.previous_time
            self.previous_time = current_time
            
            # Update performance metrics (for display)
            self.frequency = 1.0 / frame_time if frame_time > 0 else self.FPS_TARGET
            self.latency = frame_time
            
            self._fps_display_accumulator += frame_time
            if self._fps_display_accumulator >= 0.2:
                self._fps_display_accumulator = 0.0
                if self.frequency < self.FPS_TARGET + 20:
                    self.displayed_FPS = self.frequency
                else:
                    self.displayed_FPS = float(self.FPS_TARGET)
            
            # Add to accumulator (only if not paused)
            if not self.is_paused:
                self.time_accumulator += frame_time
            
            # Limit accumulator to prevent spiral of death
            if self.time_accumulator > self.max_accumulation:
                self.time_accumulator = self.max_accumulation

            # ===== UPDATE KEYS MAP =====
            if state.engine.config_panel is None or not state.engine.config_panel.visible:
                self.KEY_MAP[pygame.K_ESCAPE] = ActionManager.quit_engine
            else:
                self.KEY_MAP[pygame.K_ESCAPE] = state.engine.config_panel.toggle
            
            # ===== EVENT HANDLING =====
            events_list = []
            for event in pygame.event.get():
                self.handle_input(event)
                events_list.append(event)
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

            # ===== UPDATE CONFIG PANEL =====
            if hasattr(self, 'config_panel') and self.config_panel:
                self.config_panel.update(events_list)

            # ===== CHECK HELP KEYS (HOLD TO DISPLAY) =====
            keys = pygame.key.get_pressed()
            self.show_help = keys[pygame.K_h] or keys[pygame.K_i]

            # ===== PAN CAMERA =====
            if state.engine.camera.is_panning:
                mx, my = pygame.mouse.get_pos()
                state.engine.camera.update_pan(mx, my)
            
            # ===== SELECTION MANAGEMENT =====
            # Ensure only one body is selected at a time
            for circle in state.circles:
                if circle.is_selected:
                    self.circle_selected = True
                    for other in state.circles:
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
                for circle in state.circles:
                    if self.temp_circle.is_colliding_with(circle):
                        self.collision_detected = True
                        break
                
                if self.collision_detected:
                    state.circles.append(self.temp_circle)
                    self.temp_circle = None
                    self.mouse_down = False
                    self.mouse_down_start_time = None
            
            # ===== PHYSICS (fixed timestep - precise only, with optional substeps) =====
            # Do as many physics steps as needed to catch up
            if not self.is_paused:
                # Precise mode: original behavior (regular calculations)
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
                    
                    self.physics_step_with_substeps(self.physics_timestep)
                    self.time_accumulator -= self.physics_timestep
                    physics_steps += 1
                
                # Perdre le temps restant si limite atteinte
                if physics_steps >= max_steps_per_frame:
                    self.time_accumulator = 0.0
            
            # ===== RENDERING =====
            # Calculate interpolation alpha for smooth rendering
            # alpha = how far we are between current and next physics state
            if self.use_interpolation:
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

            # ===== DRAW CONFIG PANEL (OVERLAY) =====
            if hasattr(self, 'config_panel') and self.config_panel:
                self.config_panel.draw()
            
            # Update display and maintain target FPS
            pygame.display.flip()
            clock.tick(self.FPS_TARGET)
        
        # Clean exit
        ActionManager.quit_engine()


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

    # Create and run the simulation engine
    engine = Engine()
    Logger.info("Engine initialized")

    try:
        state.engine.run()
    except Exception as e:
        Logger.exception(f"Engine crashed in main loop: {e}")
        raise e
    