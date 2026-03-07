# Gravity Engine

## Version 3.3.5 - Camera and Random Generation Edition

A real-time N-body gravitational simulation with camera system, zoom-adaptive generation, and interactive help overlay.

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
- [What's New in v3.3.0](#whats-new-in-v330)
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

## 🪶 Before We Begin

Hello, I am 15 years old and passionate about programming and physics. In mid-2025, I decided to create a gravity simulator with Python. This is the result of my work. Feel free to submit pull requests if you identify potential improvements or optimization opportunities. I am constantly improving it, and I hope you like it.

Every previous change is documented in [ROADMAP.md](ROADMAP.md).

---

## Overview

Gravity Engine is an interactive N-body gravitational simulation that allows you to create and observe celestial bodies interacting under Newtonian gravity. Watch bodies orbit, collide, and merge in real-time with accurate physics and smooth visualization.

### Key Technical Features

- **Interactive help overlay** - Hold H or I for instant control reference
- **Complete camera system** - Pan, zoom, reset with smooth transitions
- **Zoom-adaptive generation** - Body masses scale with zoom level
- **Screen-constant growth** - Bodies grow at constant visual rate
- **Mass-proportional energy** - Heavy bodies move realistically
- **Fixed timestep physics** - Deterministic simulation (1/120s per step)
- **Complete interpolation** - Position, velocity, force, and radius smoothly interpolated
- **Visual collision detection** - Detects collisions on what you see
- **Adaptive performance mode** - Maintains 120 FPS even with 100+ bodies

---

## What's New in v3.3.0

### Interactive Complete Camera and Help System (February 2026 (was previous for April))

**Major Feature:** Advanced camera system with a new random generation mode Real-time help overlay accessible anytime during simulation.

#### Interactive Advanced Camera System
**Camera navigation (pan, zoom, reset)**
- Press A or E to zoom in or zoom out
- Use the arrows or the right button to move the camera
- Use T to reset mouse zoom and position

#### Interactive Help Overlay

**Instant Access:**
- Hold **H** or **I** to display complete controls guide
- Release to return to simulation immediately
- No interruption to physics simulation

**Professional Design:**
- Semi-transparent dark overlay
- Organized sections (Mouse, Camera, Simulation, Other)
- Color-coded controls (green keys, white descriptions)
- Centered layout with clear separation

**Comprehensive Coverage:**
- All mouse controls (click, drag, zoom)
- Camera navigation (pan, zoom, reset)
- Simulation controls (pause, vectors, random mode)
- System commands (delete, exit)

#### User Experience Improvements

**Visual Indicator:**
- "Hold H or I to display help" shown in top-right corner
- Subtle red text to indicate availability
- Always visible but unobtrusive

**Smooth Integration:**
- Help overlay pauses interactions but not physics
- Information remains accessible during simulation
- No need to exit or pause to view controls

**Design Philosophy:**
- Hold to display = temporary reference
- Release to dismiss = fluid workflow
- No toggle state = intuitive behavior

---

## Features

### Current Features (April 2026 - v3.3.0)

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
- World ↔ screen coordinate conversion

**Random Generation:**
- Zoom-adaptive body masses (mass ∝ 1/scale²)
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
- Mass-proportional energy (E ∝ mass)
- Heavy bodies move realistically
- Proportional kinetic energy distribution
- Adjustable energy per kilogram

**Physics Engine:**
- Real-time N-body gravitational simulation with O(n²) calculations
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

### Recent Improvements (v3.3.0)

- **Complete camera system** - Pan, zoom, reset with coordinate conversion
- **Zoom-adaptive generation** - Body masses scale with zoom level
- **Interactive help overlay** - Hold H/I for instant control reference
- **Visual help indicator** - Top-right corner reminder
- **Smooth help integration** - No simulation interruption
- **Professional help design** - Semi-transparent, organized, color-coded
- **Comprehensive coverage** - All controls documented in-app

### Recent Improvements (v3.2.0)

- **Screen-constant growth** - Visual growth rate independent of zoom
- **Mass-proportional energy** - Heavy bodies move realistically (E ∝ mass)
- **Radius interpolation fix** - No more flicker during body creation

---

## Installation

### Option 1: Use Pre-built Executable (Easiest)

For Windows users:

1. Download `GravityEngine.exe` from [Releases](https://github.com/Nitr0xis/GravityEngine/releases)
2. Double-click to run - no installation needed
3. Press **H** or **I** in-app for controls guide

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

# Press H or I in-app for controls
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

### Using the Build Menu (Recommended)

Double-click `make.bat` to access the interactive build system:

```
================================================
  Gravity Engine - Build System
  by Nils DONTOT
================================================

[1] Build Development      (with console)
[2] Build Release          (ready to distribute)
[3] Clean                  (remove build files)
[4] Clean + Build Release  (fresh release build)
[5] Run                    (without building)
[6] Test Executable        (run last built .exe)
[7] Open dist folder       (view executables)
[8] Help
[0] Exit

================================================
```

### Build Options

| Option | Purpose | Output | Use Case |
|--------|---------|--------|----------|
| **[1] Development** | Quick build with debug console | `GravityEngine_Dev.exe` | Testing, debugging |
| **[2] Release** | Optimized, no console | `GravityEngine.exe` | Distribution |
| **[3] Clean** | Remove build artifacts | - | Fresh start |
| **[4] Clean + Build** | Clean then release build | `GravityEngine.exe` | Final distribution |
| **[5] Run** | Launch Python source | - | Quick testing |
| **[6] Test Executable** | Run last built .exe | - | Verify build |
| **[7] Open dist/** | Open folder in Explorer | - | View executables |

---

## Controls

**💡 TIP: Press and hold H or I during simulation for complete controls guide!**

### Mouse Controls

| Action | Effect |
|--------|--------|
| **Left Click** | Select body / Create body (on empty space) |
| **Left Hold** | Increase body size exponentially (screen-constant growth) |
| **Right Click + Drag** | Pan camera view |
| **Mouse Wheel Up** | Zoom in (centered on cursor) |
| **Mouse Wheel Down** | Zoom out (centered on cursor) |

Note: Click detection uses visual positions (interpolated), not physical positions.

### Keyboard Controls

| Key | Action |
|-----|--------|
| **H / I** | **Display help overlay (hold to show, release to hide)** |
| **Space** | Pause/unpause simulation |
| **V** | Toggle velocity vectors |
| **R** | Toggle random velocity mode (mass-proportional) |
| **G** | Toggle reversed gravity |
| **P** | Generate random environment (20 bodies, zoom-adaptive) |
| **T** | Reset camera to default position and zoom |
| **A** | Zoom in (screen-centered) |
| **E** | Zoom out (screen-centered) |
| **↑ ← ↓ →** | Pan camera with arrow keys |
| **Delete** | Delete selected body |
| **Escape** | Exit program |

---

## Configuration

Modify parameters in `Engine.__init__()` within `src/gravity_engine.py`.

### Key Configuration Sections

**Camera Settings:**
```python
self.camera_basic_scale = 1.0        # Default zoom level
self.camera_scale_factor = 1.1       # Zoom step multiplier
self.camera.min_scale = 0.001        # Minimum zoom (max zoom out)
self.camera.max_scale = 100.0        # Maximum zoom (max zoom in)
self.camera_speed = 10               # Arrow key pan speed (pixels/frame)
```

**Random Generation:**
```python
self.random_energy_per_kg = 1e-8     # Energy per kilogram (J/kg)
self.random_mass_field = 1e7         # Max mass at zoom 1.0 (kg)
self.random_environment_number = 20  # Bodies created with P key
```

**Body Creation:**
```python
self.growing_speed = 0.1             # Growth rate (pixels/frame base)
self.minimum_mass = 1e3              # Minimum body mass (kg)
self.default_density = 5.514e3       # Default density (kg/m³, Earth)
```

**Performance Mode:**
```python
self.performance_mode = "precise"    # or "adaptive"
# - "precise": Fixed 120 Hz, deterministic, may slow with many bodies
# - "adaptive": Throttled updates (40 Hz), smooth, less accurate

self.min_physics_interval = 0.025    # 25ms = 40 Hz (adaptive mode)
```

**Physics Settings:**
```python
self.G = 6.6743e-11                  # Gravitational constant
self.time_acceleration = 2e4         # Time speed factor
self.fusions = True                  # Enable body fusion
```

---

## Quick Start Guide

### First Launch

1. Run `src/gravity_engine.py` or `dist/GravityEngine.exe`
2. Wait for splash screen (3 seconds)
3. **Press and hold H or I to see complete controls guide**
4. Click and hold to create a body (growth is screen-constant)
5. Press P to generate random system (20 bodies, zoom-adaptive)
6. Use mouse wheel to zoom in/out
7. Right-click drag to pan the view
8. Click a body to see detailed information
9. Press V to see vectors (red = velocity, blue = force)
10. Press Space to pause and analyze
11. Press T to reset camera view

### Using the Help System

**Access Help:**
- Press and **hold** H or I key
- Complete controls guide appears instantly
- Organized by category for easy reference

**Navigate Help:**
- Read all controls without leaving simulation
- Physics continues running in background
- No need to memorize all keys

**Return to Simulation:**
- Simply **release** H or I
- Help disappears immediately
- Resume normal interaction

### Camera Navigation

**Exploring Large Simulations:**
1. Generate 100+ bodies (press P five times)
2. Zoom out (mouse wheel down) to see overview
3. Pan to interesting region (right-click drag)
4. Zoom in (mouse wheel up) on specific bodies
5. Press T to return to default view

**Creating at Different Scales:**
1. Zoom out (bodies will be heavier automatically)
2. Create large bodies (hold 3-5 seconds)
3. Zoom in (bodies will be lighter automatically)
4. Create small bodies (hold 1-2 seconds)
5. All bodies appear similar size visually!

### Creating Systems

**Binary System:**
1. Create two medium bodies (hold 2-3 seconds each)
2. Place close but not touching
3. Watch them orbit
4. Enable vectors (V) to see motion
5. Zoom out to see full orbits

**Chaotic Three-Body:**
1. Create three similar-sized bodies
2. Arrange in triangle
3. Press R for random mode
4. Add more bodies for chaos
5. Use camera to follow the action

**Central Star:**
1. Zoom out 10× (mouse wheel down)
2. Create one large central body (hold 5+ seconds)
3. Zoom back in (mouse wheel up)
4. Add smaller bodies around it
5. Disable fusion in config to prevent merging
6. Enable random mode for orbits

**Large Simulation (100+ bodies):**
1. Switch to adaptive mode in config
2. Press P repeatedly (20 bodies each time)
3. Zoom out to see overview
4. Enjoy smooth 120 FPS
5. Pan to explore different regions

---

## Educational Use

Gravity Engine demonstrates:

1. **Newton's Law of Universal Gravitation** - F = G(m₁m₂)/r²
2. **Momentum Conservation** - Total momentum before = after
3. **Fixed Timestep Integration** - Deterministic physics
4. **Linear Interpolation** - Smooth rendering between states
5. **Coordinate Transformation** - World ↔ screen conversion
6. **Zoom-Adaptive Scaling** - Mass scales with view scale
7. **Mass-Energy Relationship** - E = ½mv², E ∝ mass for fair dynamics
8. **Vector Mathematics** - Force and velocity decomposition
9. **N-body Problem** - Classical unsolved problem
10. **Visual Collision Detection** - Interpolated collision checking
11. **Interactive UI Design** - Help overlay, real-time feedback
12. **User Experience** - Intuitive controls, smooth interactions

Perfect for:
- Physics education (Newton's laws, gravity, coordinate systems)
- Programming learning (game physics, Pygame, Python, UI design)
- Mathematics (vectors, trigonometry, integration, logarithms)
- Computational thinking (optimization, algorithms, spatial transformations)
- User interface design (help systems, overlays, visual feedback)

---

## Troubleshooting

### Common Issues

**Font not found:**
- Ensure `assets/fonts/main_font.ttf` exists
- Check file paths are correct

**Help overlay not showing:**
- Make sure you're **holding** H or I (not just pressing)
- Release key to dismiss
- Check that fonts are properly loaded

**Simulation too fast/slow:**
- Adjust `self.time_acceleration` in config
- Default: 2e4 (20,000× real time)

**Poor performance:**
- Switch to adaptive mode
- Reduce physics frequency: `self.min_physics_interval = 0.050`
- Disable vectors (V key)
- Lower FPS: `self.FPS_TARGET = 60`

**Bodies too small after zooming out:**
- Fixed in v3.2.0 with zoom-adaptive generation
- Press P after zooming to generate appropriate bodies
- Body masses now scale with zoom²

**Body growth invisible when zoomed out:**
- Fixed in v3.2.0 with screen-constant growth
- Growth rate now adapts to zoom level
- Visual growth speed is constant

**Heavy bodies don't move in random mode:**
- Fixed in v3.2.0 with mass-proportional energy
- Energy now scales with mass (E ∝ mass)
- Heavy bodies move realistically

---

## Roadmap (Can release sooner)

See [ROADMAP.md](ROADMAP.md) for complete development plans.

### Recently Completed (v3.3.0 - February 2026)

**Interactive Help System:**
- Real-time help overlay (hold H or I)
- Professional semi-transparent design
- Organized controls by category
- Visual availability indicator
- Smooth integration with simulation

**Camera System:**
- Complete pan, zoom, reset functionality
- World ↔ screen coordinate conversion
- Cursor-centered mouse wheel zoom
- Screen-centered keyboard zoom (A/E)
- Arrow key camera movement

**Random Generation:**
- Zoom-adaptive body masses (mass ∝ 1/scale²)
- Logarithmic mass distribution
- World-coordinate generation
- Bodies always fill visible screen

**Body Creation:**
- Screen-constant growth rate
- Visual growth independent of zoom
- Smooth radius interpolation fix

**Random Mode:**
- Mass-proportional energy (E ∝ mass)
- Heavy bodies move realistically
- Proportional kinetic energy distribution

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
git clone https://github.com/Nitr0xis/GravityEngine.git

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

- HIGH: Save/load system (May 2026)
- MEDIUM: Enhanced camera features (May 2026)
- MEDIUM: Scenario presets (May 2026)
- LOW: Visual effects (July 2026)

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

*Last updated: February 25, 2026*
*Version: 3.3.5 - Camera and Random Generation Edition*

---

*Enjoy exploring gravitational physics!*
