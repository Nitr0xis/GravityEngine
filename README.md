# Gravity Engine

## Version 3.5.0 - Complete Configuration Panel Edition

A real-time N-body gravitational simulation with camera system, pygame configuration panel, and interactive help overlay.

**Created by Nils DONTOT**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)](https://www.pygame.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Nitr0xis-181717?logo=github)](https://github.com/Nitr0xis)

---

**Author:** Nils DONTOT (15 years old)  
**Repository:** [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)  
**Email:** [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)

---

## Table of Contents

- [Before We Begin](#before-we-begin)
- [Overview](#overview)
- [What's New in v3.5.0](#whats-new-in-v350)
- [Features](#features)
- [Installation](#installation)
- [Building Executables](#building-executables)
- [Controls](#controls)
- [Configuration](#configuration)
- [Physics](#physics)
- [Performance Modes](#performance-modes)
- [Quick Start Guide](#quick-start-guide)
- [Troubleshooting](#troubleshooting)
- [Educational Use](#educational-use)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Before We Begin

Hello, I am 15 years old and passionate about programming and physics. In mid-2025, I decided to create a gravity simulator with Python. This is the result of my work. Feel free to submit pull requests if you identify potential improvements or optimization opportunities. I am constantly improving it, and I hope you like it.

Every previous change is documented in [ROADMAP.md](ROADMAP.md).

---

## Overview

Gravity Engine is an interactive N-body gravitational simulation that allows you to create and observe celestial bodies interacting under Newtonian gravity. Watch bodies orbit, collide, and merge in real-time with accurate physics and smooth visualization.

### Key Technical Features

- **Pygame configuration panel** - Real-time parameter adjustment with custom widgets
- **Interactive help overlay** - Hold H or I for instant control reference
- **Atlas file manager** - Cross-platform file management (dev + exe)
- **Screenshot system** - Capture simulations with S key
- **Complete camera system** - Pan, zoom, reset with smooth transitions
- **Zoom-adaptive generation** - Body masses scale with zoom level
- **Screen-constant growth** - Bodies grow at constant visual rate
- **Mass-proportional energy** - Heavy bodies move realistically
- **Fixed timestep physics** - Deterministic simulation (1/120s per step)
- **Complete interpolation** - Position, velocity, force, and radius smoothly interpolated
- **Visual collision detection** - Detects collisions on what you see
- **Adaptive performance mode** - Maintains 120 FPS even with 100+ bodies

---

## What's New in v3.5.0

### Pygame Configuration Panel (May 2026)

**Major Feature:** Professional overlay-style configuration panel built entirely in Pygame.

#### Custom Widget System

**Widgets Implemented:**
- Animated checkboxes with smooth fade-in/fade-out
- Linear and logarithmic sliders with real-time value display
- Buttons with hover effects
- Scrollable content panel
- Semi-transparent overlay design

**Visual Design:**
- Matches Gravity Engine color scheme (ducky green accents)
- Dark theme with professional appearance
- Smooth animations on all interactions
- Responsive to mouse hover and drag

#### Configuration Features

**Real-Time Adjustment:**
- Modify parameters while simulation runs
- See changes immediately in the background
- No interruption to physics or rendering
- Smooth overlay appearance/disappearance

**Sections:**
- Simulation: Time acceleration, Target FPS
- Physics: Default density, Body fusions toggle
- Visual: Vector display, Force vectors, Vector scale

**Persistence:**
- Save configuration to JSON (user_data/config.json)
- Load saved configurations
- Automatic file management via Atlas

#### User Experience

**Opening/Closing:**
- Press C to toggle panel
- Press ESC to close
- Click outside panel to close
- Overlay dims simulation background

**Interaction:**
- Drag sliders to adjust values
- Click checkboxes to toggle
- Mouse wheel to scroll if needed
- Visual feedback on hover

### Atlas File Manager Integration

**Cross-Platform Paths:**
- Automatic dev/exe detection
- User data in Documents folder (exe)
- User data in project folder (dev)
- Resource path resolution for assets

**Folder Management:**
- Screenshots folder created automatically
- Saves folder for future save/load
- Logs folder for debugging
- Config file storage

### Screenshot System

**Capture Functionality:**
- Press S to take screenshot
- Automatic timestamped filenames
- Saved to screenshots folder
- Confirmation message displayed
- Full resolution capture

---

## Features

### Current Features (May 2026 - v3.5.0)

**Configuration Panel:**
- Pygame-based overlay interface
- Custom animated widgets (checkboxes, sliders, buttons)
- Real-time parameter adjustment
- Save/load configuration to JSON
- Scrollable content support
- Professional dark theme matching simulation
- No external windows or dependencies

**File Management:**
- Atlas module for cross-platform paths
- Automatic folder creation (screenshots, saves, logs)
- Dev mode: files in project folder
- Exe mode: files in Documents folder
- Resource path resolution for assets

**Screenshot System:**
- One-key screenshot capture (S)
- Automatic file naming with timestamp
- Saved to managed screenshots folder
- Visual confirmation message
- Full resolution PNG format

**Interactive Help:**
- Real-time help overlay (hold H or I)
- Comprehensive controls reference
- Professional semi-transparent design
- Organized by category (Mouse, Camera, Simulation)
- Always accessible without interrupting simulation

**Camera System:**
- Pan view with right-click drag
- Zoom with mouse wheel (cursor-centered)
- Keyboard zoom A/E (screen-centered)
- Arrow keys for camera movement
- Reset camera with T key
- Smooth camera transitions
- World to screen coordinate conversion

**Random Generation:**
- Zoom-adaptive body masses (mass proportional to 1/scale squared)
- Logarithmic mass distribution
- World-coordinate generation
- Bodies always fill visible screen
- Realistic body size variety

**Body Creation:**
- Screen-constant growth rate
- Visual growth independent of zoom
- Smooth radius interpolation
- Exponential acceleration while holding
- Mass calculated from radius and density

**Random Mode:**
- Mass-proportional energy (E proportional to mass)
- Heavy bodies move realistically
- Proportional kinetic energy distribution
- Adjustable energy per kilogram

**Physics Engine:**
- Real-time N-body gravitational simulation with O(n squared) calculations
- Fixed timestep integration (1/120s) for deterministic behavior
- Complete interpolation system (position, velocity, force, radius)
- Momentum and mass conservation in all interactions
- Time acceleration system (configurable speed)

**Rendering:**
- Smooth 120 FPS display with alpha blending
- Interpolation cache for optimal performance
- Vector visualization (velocity in red, forces in blue)
- Cardinal velocity components (X in green, Y in yellow)
- Dark/light color schemes
- Culling optimization (off-screen bodies not rendered)

**Interaction:**
- Interactive body creation (click and hold, exponential growth)
- Body selection with detailed information panel
- Visual collision detection on interpolated positions
- Interpolated click detection (select bodies where you see them)
- Camera navigation (pan, zoom, reset)
- Pause/resume for analysis

**Modes:**
- **Precise mode** - Fixed 120 Hz physics, high accuracy
- **Adaptive mode** - Throttled physics (default 40 Hz), smooth rendering
- **Random velocity mode** - Mass-proportional chaotic initial conditions
- **Reversed gravity** - Repulsion instead of attraction

**Testing:**
- 7 comprehensive unit tests
- Physics validation (force summation, determinism, uniform speed)
- Interpolation validation (position, velocity, force, cache)

### Recent Improvements (v3.4.0)

- **Pygame configuration panel** - Professional overlay with custom widgets
- **Atlas file manager** - Cross-platform file path management
- **Screenshot system** - One-key capture with auto-naming
- **Config persistence** - Save/load settings to JSON
- **Real-time adjustment** - Change parameters without interrupting simulation

### Recent Improvements (v3.3.0)

- **Interactive help overlay** - Hold H/I for instant control reference
- **Visual help indicator** - Top-right corner reminder
- **Smooth help integration** - No simulation interruption
- **Professional help design** - Semi-transparent, organized, color-coded
- **Comprehensive coverage** - All controls documented in-app

### Recent Improvements (v3.2.0)

- **Complete camera system** - Pan, zoom, reset with coordinate conversion
- **Zoom-adaptive generation** - Body masses scale with zoom level
- **Screen-constant growth** - Visual growth rate independent of zoom
- **Mass-proportional energy** - Heavy bodies move realistically (E proportional to mass)
- **Radius interpolation fix** - No more flicker during body creation

---

## Installation

### Option 1: Use Pre-built Executable (Easiest)

For Windows users:

1. Download `GravityEngine.exe` from [Releases](https://github.com/Nitr0xis/GravityEngine/releases)
2. Double-click to run - no installation needed
3. Press **C** for configuration panel
4. Press **H** or **I** for controls guide
5. Press **S** to capture screenshots

Note: The executable is self-contained with all dependencies included.

### Option 2: Run from Source (For Developers)

**Prerequisites:**
- Python 3.11+
- pip package manager

**Steps:**

```bash
# Clone repository
git clone https://github.com/Nitr0xis/GravityEngine.git
cd GravityEngine

# Install dependencies (or let the program auto-install)
pip install pygame

# Run simulation
python src/gravity_engine.py

# Press C for config, H for help, S for screenshot
```

### Option 3: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install and run
pip install pygame
python src/gravity_engine.py
```

## Building Executables

### Using PyInstaller

Build a standalone executable with all dependencies:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --add-data "assets;assets" --name GravityEngine src/gravity_engine.py

# Executable will be in dist/ folder
```

**Notes:**
- `--onefile`: Single executable file
- `--windowed`: No console window
- `--add-data`: Include assets folder
- Exe includes all dependencies automatically

---

## Controls

### Configuration

| Key | Action |
|-----|--------|
| C | Open/close configuration panel |

**Configuration Panel:**
- Click and drag sliders to adjust values
- Click checkboxes to toggle options
- Mouse wheel to scroll (if needed)
- Save button: Store current config
- Load button: Restore saved config
- Close button: Exit panel

### Help System

| Key | Action |
|-----|--------|
| H or I (hold) | Display interactive help overlay |

### Camera Navigation

| Input | Action |
|-------|--------|
| Right Click + Drag | Pan camera view |
| Mouse Wheel Up | Zoom in (cursor-centered) |
| Mouse Wheel Down | Zoom out (cursor-centered) |
| A | Zoom in (screen-centered) |
| E | Zoom out (screen-centered) |
| Arrow Keys | Pan camera (Up/Down/Left/Right) |
| T | Reset camera to default position and zoom |

### Body Interaction

| Input | Action |
|-------|--------|
| Left Click | Select body OR create new body (on empty space) |
| Left Click + Hold | Increase body size exponentially |
| Delete | Delete selected body |

### Simulation Control

| Key | Action |
|-----|--------|
| Space | Pause/unpause simulation |
| V | Toggle velocity/force vectors display |
| R | Toggle random velocity mode |
| G | Toggle reversed gravity (repulsion) |
| P | Generate 20 random bodies (zoom-adaptive) |
| S | Take screenshot (saved to screenshots folder) |

### System

| Key | Action |
|-----|--------|
| Escape | Exit program |
| Alt + F4 | Exit program (Windows) |

---

## Configuration

### Using the Configuration Panel

**Access:**
1. Press **C** to open panel
2. Panel appears as overlay on simulation
3. Simulation continues running in background

**Available Settings:**

**Simulation Section:**
- **Time Acceleration** - Simulation speed multiplier (1e3 to 1e8, logarithmic)
- **Target FPS** - Rendering frames per second (30 to 240, linear)

**Physics Section:**
- **Default Density** - Body density in kg/m³ (1e2 to 1e5, logarithmic)
- **Enable Body Fusions** - Toggle collision merging (checkbox)

**Visual Section:**
- **Show Velocity Vectors** - Display red velocity arrows (checkbox)
- **Show Force Vectors** - Display blue force arrows (checkbox)
- **Vector Scale** - Adjust vector length multiplier (0.1 to 10.0, linear)

**Saving Configuration:**
1. Adjust parameters as desired
2. Click **Save** button
3. Settings stored in `user_data/config.json`
4. Click **Load** to restore saved settings

### Manual Configuration (Advanced)

Edit parameters directly in `gravity_engine.py`:

```python
# In Engine.__init__()

# Simulation
self.time_acceleration = 2e4  # Simulation speed
self.FPS_TARGET = 120  # Rendering FPS

# Physics
self.default_density = 5.514e3  # kg/m³ (Earth density)
self.fusions = True  # Enable body merging
self.minimum_mass = 1e3  # Minimum body mass (kg)

# Visual
self.vectors_printed = False  # Show vectors
self.force_vectors = True  # Show force vectors
self.vector_scale = 1.0  # Vector length multiplier
self.use_interpolation = True  # Smooth rendering

# Performance
self.performance_mode = "precise"  # "precise" or "adaptive"
self.min_physics_interval = 0.025  # 40 Hz physics (adaptive mode)

# Camera
self.camera_speed = 10  # Arrow key pan speed
self.camera_scale_factor = 1.1  # Zoom step multiplier

# Random
self.random_mode = False  # Random velocity on creation
self.random_energy_per_kg = 1e-8  # J/kg for random velocities
self.random_mass_field = 1e7  # Maximum random mass range
self.random_environment_number = 20  # Bodies generated per P press
```

---

## Physics

### Gravitational Force

Newton's law of universal gravitation:

```
F = G × (m1 × m2) / r²
```

Where:
- F = gravitational force (Newtons)
- G = gravitational constant (6.674 × 10⁻¹¹ N⋅m²/kg²)
- m1, m2 = masses of the two bodies (kg)
- r = distance between centers (meters)

### Integration Method

**Fixed Timestep (Precise Mode):**
- Physics calculated every 1/120 seconds
- Deterministic behavior
- Position: x(t+dt) = x(t) + v(t) × dt
- Velocity: v(t+dt) = v(t) + a(t) × dt
- Acceleration: a = F / m

**Adaptive Mode:**
- Physics throttled to 40 Hz (configurable)
- Rendering still 120 FPS
- Accumulates time between updates
- Smooth visuals, acceptable accuracy

### Interpolation System

**Complete State Interpolation:**
- Position: x_render = x_prev + (x - x_prev) × alpha
- Velocity: v_render = v_prev + (v - v_prev) × alpha
- Force: f_render = f_prev + (f - f_prev) × alpha
- Radius: r_render = r_prev + (r - r_prev) × alpha

Where alpha = time_accumulator / physics_timestep (0 to 1)

### Collision and Fusion

**Detection:**
- Visual: Check interpolated positions
- Physical: Verify real positions
- Fusion only if both collide

**Fusion Physics:**
- Conservation of momentum: p_total = p1 + p2
- Conservation of mass: m_total = m1 + m2
- New position: Center of mass
- New velocity: Total momentum / total mass
- New radius: Calculated from volume and density

---

## Performance Modes

### Precise Mode (Default)

**Characteristics:**
- Fixed 120 Hz physics updates
- Deterministic simulation
- Accurate long-term behavior
- May slow down with many bodies (100+)

**Best for:**
- Accurate simulations
- Scientific demonstrations
- Small to medium body counts (< 50)

**Configuration:**
```python
self.performance_mode = "precise"
```

### Adaptive Mode

**Characteristics:**
- Throttled physics (40 Hz default, configurable)
- Smooth 120 FPS rendering always
- Less accurate over long time periods
- Handles 100+ bodies smoothly

**Best for:**
- Large simulations (100+ bodies)
- Visual demonstrations
- Performance priority over accuracy

**Configuration:**
```python
self.performance_mode = "adaptive"
self.min_physics_interval = 0.025  # 40 Hz (25ms between updates)
```

---

## Quick Start Guide

### First Launch

**Getting Oriented:**
1. Launch the program
2. Press **H** or **I** (hold) to see controls
3. Release to continue
4. Press **C** to explore configuration panel
5. Close panel to return to simulation

### Creating Your First System

**Binary Orbit:**
1. Left-click and hold for 2 seconds (creates first body)
2. Release mouse
3. Left-click another location and hold 2 seconds (second body)
4. Watch them orbit each other
5. Press **V** to see velocity vectors

### Using the Camera

**Exploring Large Simulations:**
1. Press **P** five times (generates 100 bodies)
2. Scroll mouse wheel down to zoom out
3. Right-click and drag to pan around
4. Scroll mouse wheel up to zoom in on interesting regions
5. Press **T** to reset view

### Adjusting Parameters

**Real-Time Tweaking:**
1. Press **C** to open configuration
2. Drag "Time Acceleration" slider to speed up/slow down
3. Uncheck "Enable Body Fusions" to prevent merging
4. Adjust "Vector Scale" to make arrows more visible
5. Click **Save** to keep settings for next time

### Capturing Your Work

**Taking Screenshots:**
1. Create interesting configuration
2. Press **S** key
3. Screenshot saved automatically to screenshots folder
4. Confirmation message appears
5. Find images in: Documents/GravityEngine/screenshots/ (exe) or user_data/screenshots/ (dev)

---

## Educational Use

Gravity Engine demonstrates:

1. **Newton's Law of Universal Gravitation** - F = G(m1×m2)/r²
2. **Momentum Conservation** - Total momentum before equals after
3. **Fixed Timestep Integration** - Deterministic physics
4. **Linear Interpolation** - Smooth rendering between states
5. **Coordinate Transformation** - World to screen conversion
6. **Zoom-Adaptive Scaling** - Mass scales with view scale
7. **Mass-Energy Relationship** - E = 0.5mv², E proportional to mass
8. **Vector Mathematics** - Force and velocity decomposition
9. **N-body Problem** - Classical unsolved problem
10. **Visual Collision Detection** - Interpolated collision checking
11. **UI Design Principles** - Overlay panels, custom widgets
12. **File Management** - Cross-platform path resolution

Perfect for:
- Physics education (Newton's laws, gravity, coordinate systems)
- Programming learning (game physics, Pygame, Python, UI design)
- Mathematics (vectors, trigonometry, integration, logarithms)
- Computational thinking (optimization, algorithms, transformations)
- User interface design (configuration panels, help systems, widgets)

---

## Troubleshooting

### Common Issues

**Configuration panel not opening:**
- Make sure you press **C** (not Ctrl+C)
- Check console for error messages
- Verify config_panel_pygame.py is in src/ folder

**Font not found:**
- Ensure `assets/fonts/main_font.ttf` exists
- Check file paths are correct
- Verify Atlas is resolving paths properly

**Help overlay not showing:**
- Make sure you're **holding** H or I (not just pressing)
- Release key to dismiss
- Check that fonts are properly loaded

**Simulation too fast/slow:**
- Press **C** to open config panel
- Adjust Time Acceleration slider
- Default: 2e4 (20,000× real time)
- Or edit `self.time_acceleration` in code

**Poor performance:**
- Switch to adaptive mode in config
- Reduce physics frequency: `self.min_physics_interval = 0.050`
- Disable vectors (V key)
- Lower FPS via config panel

**Screenshots not saving:**
- Check user_data/screenshots/ folder exists
- Verify Atlas file manager initialized
- Check console for error messages
- Ensure write permissions in Documents folder (exe)

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for complete development plans.

### Recently Completed (v3.4.0 - May 2026)

**Configuration Panel:**
- Pygame-based overlay interface
- Custom animated widgets
- Real-time parameter adjustment
- Save/load to JSON
- Professional dark theme

**File Management:**
- Atlas module integration
- Cross-platform path resolution
- Automatic folder creation
- Dev/exe mode detection

**Screenshot System:**
- One-key screenshot capture
- Automatic file naming
- Managed folder storage

### Recently Completed (v3.3.0 - April 2026)

**Interactive Help System:**
- Real-time help overlay (hold H or I)
- Professional semi-transparent design
- Organized controls by category
- Visual availability indicator
- Smooth integration with simulation

### Recently Completed (v3.2.0 - March 2026)

**Camera System:**
- Complete pan, zoom, reset functionality
- World to screen coordinate conversion
- Cursor-centered mouse wheel zoom
- Screen-centered keyboard zoom (A/E)
- Arrow key camera movement

**Random Generation:**
- Zoom-adaptive body masses (mass proportional to 1/scale²)
- Logarithmic mass distribution
- World-coordinate generation
- Bodies always fill visible screen

**Body Creation:**
- Screen-constant growth rate
- Visual growth independent of zoom
- Smooth radius interpolation fix

**Random Mode:**
- Mass-proportional energy (E proportional to mass)
- Heavy bodies move realistically
- Proportional kinetic energy distribution

### Current Focus (June 2026)

| Priority | Feature | Status |
|----------|---------|--------|
| 1 | Save/load scenarios (JSON) | In Progress |
| 2 | Predefined scenario presets | Planned |
| 3 | Performance profiling | Planned |
| 4 | Enhanced data export (CSV) | Planned |

### Next Milestones

- **June 2026**: Save/load system, scenario presets
- **July 2026**: Performance optimization, data export
- **Q3 2026**: Visual effects, analysis tools, comprehensive documentation

---

## Contributing

Contributions are welcome! Here's how:

### Ways to Contribute

1. **Report bugs** - Open detailed issues
2. **Suggest features** - Share ideas
3. **Submit pull requests** - Fix bugs or add features
4. **Improve documentation** - Clarify README
5. **Share simulations** - Show creations
6. **Optimize code** - Performance improvements

### Development Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/GravityEngine.git

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes and test
python src/gravity_engine.py

# 4. Commit and push
git commit -m "Add: feature description"
git push origin feature/your-feature

# 5. Create pull request
```

### Priority Areas

- HIGH: Save/load system (June 2026)
- HIGH: Scenario presets (June 2026)
- MEDIUM: Performance profiling (July 2026)
- MEDIUM: Data export features (July 2026)
- LOW: Visual effects (August 2026)

---

## License

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International**

[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Copyright (c) 2026 Nils DONTOT**

### You are free to:

- Share - Copy and redistribute
- Adapt - Remix, transform, build upon

### Under these terms:

- **Attribution** - Give credit to Nils DONTOT
- **NonCommercial** - No commercial use
- **ShareAlike** - Distribute under same license

See [LICENSE](LICENSE) for complete terms.

---

## Contact

**Nils DONTOT**

- Email: [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)
- GitHub: [@Nitr0xis](https://github.com/Nitr0xis)
- Repository: [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)
- Issues: [Report bugs or suggestions](https://github.com/Nitr0xis/GravityEngine/issues)

---

**⭐ Star this repository if you find it interesting!**

**Made with ❤️ and ☕ by [Nils DONTOT](https://github.com/Nitr0xis) (age 15)**

*Last updated: March 2026*  
*Version: 3.5.0 - Complete Configuration Panel Edition*

---

*Enjoy exploring gravitational physics! Press C for config, H for help, S for screenshots!*
