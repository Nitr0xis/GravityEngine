# Gravity Engine

## Version 3.1.0 - Advanced Interpolation Edition

A real-time N-body gravitational simulation with deterministic physics and complete interpolation system.

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
- [What's New in v3.1.0](#whats-new-in-v310)
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

- **Fixed timestep physics** - Deterministic simulation (1/120s per step)
- **Complete interpolation** - Position, velocity, force, and radius smoothly interpolated
- **Adaptive performance mode** - Maintains 120 FPS even with 100+ bodies
- **Visual collision detection** - Detects collisions on what you see
- **Momentum conservation** - Physically accurate collisions and mergers
- **Time accumulator** - Handles variable frame rates with "spiral of death" prevention

---

## What's New in v3.1.0

### Complete Mode PRECISE Interpolation (February 23, 2026)

**Major Feature:** All physical properties are now smoothly interpolated for perfect visual accuracy.

#### Interpolated Properties

1. **Position** (prev_x, prev_y) - Bodies move smoothly
2. **Velocity** (prev_vx, prev_vy) - Velocity vectors transition smoothly
3. **Force** (prev_force) - Force vectors change progressively
4. **Radius** (prev_radius) - Fusions appear smooth and natural

#### Technical Improvements

- **Interpolation cache** - Prevents redundant calculations per frame
- **get_interpolated_state()** - Centralized interpolation method
- **Cache invalidation** - Automatic on physics updates
- **7 unit tests** - Complete validation (3 physics + 4 interpolation)

#### Visual Benefits

- **Smooth velocity vectors** - No more sudden jumps
- **Progressive force vectors** - Forces change gradually
- **Natural fusions** - Radius grows smoothly when bodies merge
- **Perfect synchronization** - All visuals match interpolated state

---

## Features

### Current Features (February 2026 - v3.1.0)

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

**Interaction:**
- Interactive body creation (click and hold, exponential growth)
- Body selection with detailed information panel
- Visual collision detection on interpolated positions
- Interpolated click detection (select bodies where you see them)
- Pause/resume for analysis

**Modes:**
- **Precise mode** - Fixed 120 Hz physics, high accuracy
- **Adaptive mode** - Throttled physics (default 40 Hz), smooth rendering
- **Random velocity mode** - Chaotic initial conditions
- **Reversed gravity** - Repulsion instead of attraction

**Testing:**
- 7 comprehensive unit tests
- Physics validation (force summation, determinism, uniform speed)
- Interpolation validation (position, velocity, force, cache)

### Recent Improvements (v3.1.0)

- **Complete interpolation** - All properties smoothly interpolated
- **Velocity interpolation** - Velocity vectors perfectly smooth
- **Force interpolation** - Force vectors transition progressively
- **Radius interpolation** - Fusions visually smooth
- **Interpolation cache** - Performance optimization
- **4 new unit tests** - Interpolation validation
- **Comprehensive documentation** - All methods documented

---

## Installation

### Option 1: Use Pre-built Executable (Easiest)

For Windows users:

1. Download `GravityEngine.exe` from [Releases](https://github.com/Nitr0xis/GravityEngine/releases)
2. Double-click to run - no installation needed

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

### Manual Building

If you prefer command line:

```bash
# Development build (with console)
cd builders
build.bat

# Release build (no console window)
cd builders
build_release.bat

# Clean build files
cd builders
clean.bat
```

### Build Requirements

- **PyInstaller** - Automatically installed on first build
- **All assets** - Must be present in `assets/` folder:
  - `assets/fonts/main_font.ttf` (required)
  - `assets/fonts/toruk.ttf` (required)
  - `assets/icon.ico` (recommended)
  - `assets/musics/*.mp3` (optional)
- **Windows** - Build scripts are Windows batch files (.bat)

### Build Output

After building, executables are located in:
```
dist/
├── GravityEngine.exe          # Release build (distribute this)
└── GravityEngine_Dev.exe      # Development build (with console)
```

### Distribution

To distribute your build:

1. Run **Clean + Build Release** (option 4)
2. Navigate to `dist/` folder
3. Distribute `GravityEngine.exe` (self-contained, ~20-30 MB)
4. Optional: Include `README.md` for users

The executable includes:
- Python interpreter
- All dependencies (Pygame)
- All assets (fonts, icon)
- No installation required for end users
---

## Controls

### Mouse Controls

| Action | Effect |
|--------|--------|
| Left Click | Select body / Create body (on empty space) |
| Right Click | Create body (hold to grow) |
| Middle Click | Create body (hold to grow) |
| Mouse Wheel | Create smallest bodies possible
| Hold Button | Increase body size exponentially |

Note: Click detection uses visual positions (interpolated), not physical positions.

### Keyboard Controls

| Key | Action |
|-----|--------|
| Space | Pause/unpause simulation |
| V | Toggle velocity vectors |
| R | Toggle random velocity mode |
| G | Toggle reversed gravity |
| P | Generate random environment (20 bodies) |
| Delete | Delete selected body |
| Escape | Exit program |

---

## Configuration

Modify parameters in `Engine.__init__()` within `src/gravity_engine.py`.

### Key Configuration Sections

**Performance Mode:**
```python
self.performance_mode = "precise"  # or "adaptive"
# - "precise": Fixed 120 Hz, deterministic, may slow with many bodies
# - "adaptive": Throttled updates (40 Hz), smooth, less accurate

self.min_physics_interval = 0.025   # 25ms = 40 Hz (adaptive mode)
```

**Physics Settings:**
```python
self.G = 6.6743e-11                 # Gravitational constant
self.time_acceleration = 2e4         # Time speed factor
self.fusions = True                  # Enable body fusion
self.minimum_mass = 1e3              # Minimum body mass (kg)
self.default_density = 5.514e3       # Default density (kg/m³)
```

**Display Settings:**
```python
self.FPS_TARGET = 120                # Target rendering FPS
self.FULLSCREEN = True               # Fullscreen mode
self.screen_mode = "dark"            # "dark" or "light"
```

**Interpolation:**
```python
self.use_interpolation = True        # Enable smooth interpolation
```

**Visualization:**
```python
self.vectors_printed = False         # Show vectors by default
self.force_vectors = True            # Show force vectors
self.cardinal_vectors = False        # Show X/Y components
self.vector_scale = 1                # Vector size multiplier
```

**Random Generation:**
```python
self.random_mode = False             # Random initial velocities
self.random_environment_number = 20  # Bodies created with P key
max_kinetic_energy_joules = 5e-4     # Max random energy (J)
```

---

## Physics

### Fixed Timestep Integration

Physics runs at fixed intervals regardless of rendering FPS:

```python
physics_timestep = 1.0 / 120  # Always 1/120 second (8.33 ms)
```

**How it works:**
1. Time accumulator collects real frame time
2. Physics steps execute when accumulator >= timestep
3. Multiple steps per frame if needed (catching up)
4. Rendering interpolates between states

**Benefits:**
- Deterministic (same inputs = same outputs)
- FPS-independent physics accuracy
- No "time dilation" from slow frames
- Predictable behavior

### Complete Interpolation System (v3.1.0)

All properties are interpolated for smooth rendering:

```python
# Get interpolated state
state = self.get_interpolated_state(alpha)

# Interpolated properties
render_x = state['x']      # Position
render_y = state['y']
render_vx = state['vx']    # Velocity
render_vy = state['vy']
render_fx = state['fx']    # Force
render_fy = state['fy']
render_radius = state['radius']  # Radius
```

**Formula (linear interpolation):**
```python
alpha = time_accumulator / physics_timestep  # 0.0 to 1.0
interpolated = previous + (current - previous) * alpha
```

**Interpolation cache:**
- Prevents redundant calculations per frame
- Validated by alpha value
- Invalidated on physics update

### Gravitational Force

Newton's law of universal gravitation:

```
F = G × (m₁ × m₂) / r²
```

Where:
- F = gravitational force (Newtons)
- G = 6.6743 × 10⁻¹¹ m³ kg⁻¹ s⁻²
- m₁, m₂ = masses (kilograms)
- r = distance between centers (meters)

### Momentum Conservation

All interactions conserve momentum:

```
p_total = m₁v₁ + m₂v₂ = constant
```

**Fusion example:**
```python
# New velocity after merger
v_new = (m₁ × v₁ + m₂ × v₂) / (m₁ + m₂)

# New position (center of mass)
x_new = (m₁ × x₁ + m₂ × x₂) / (m₁ + m₂)

# New radius from density
volume = mass / density
radius = ((3 × volume) / (4π))^(1/3)
```

### Force Vector Visualization

Force vectors use logarithmic scaling with direction preservation:

```python
# Unit vector (direction)
force_magnitude = sqrt(fx² + fy²)
unit_x = fx / force_magnitude
unit_y = fy / force_magnitude

# Logarithmic scaling (visibility)
visual_length = log10(force_magnitude + 1) × scale

# Final vector
vector_x = unit_x × visual_length
vector_y = unit_y × visual_length
```

Benefits:
- Direction always correct (no sign loss)
- Large forces compressed
- Small forces visible

### Units Reference

| Property | Unit | Symbol | Notes |
|----------|------|--------|-------|
| Mass | Kilograms | kg | Base unit |
| Distance | Meters | m | 1 pixel = 1 meter (needs scale factor) |
| Time | Seconds | s | Accelerated by time_acceleration |
| Force | Newtons | N | F = ma |
| Velocity | Meters/second | m/s | Vector magnitude |
| Density | kg/m³ | kg/m³ | Default: 5514 (Earth) |
| Energy | Joules | J | E = ½mv² |

---

## Performance Modes

### Adaptive Mode (Default)

**Configuration:**
```python
self.performance_mode = "adaptive"
self.min_physics_interval = 0.025  # 40 Hz physics
```

**How it works:**
- Physics throttled to maximum frequency (default 40 Hz)
- Rendering stays at 120 FPS via interpolation
- Automatically adapts to CPU load

**Benefits:**
- Always smooth rendering (120 FPS)
- CPU efficient (max 40 calculations/second)
- Scalable (100+ bodies smoothly)
- Configurable update frequency

**Trade-offs:**
- Lower accuracy (large timesteps: 25ms vs 8.3ms)
- Non-deterministic (varies slightly per hardware)
- May miss fast collisions (rare with visual detection)

**Best for:**
- Large simulations (>50 bodies)
- Demonstrations
- Low-end hardware
- Smooth visual experience

### Precise Mode

**Configuration:**
```python
self.performance_mode = "precise"
```

**How it works:**
- Fixed timestep: exactly 1/120 second per step
- May do multiple steps per frame
- Slows down visually if CPU can't keep up

**Benefits:**
- High accuracy (small timesteps: 8.3ms)
- Deterministic (reproducible results)
- Predictable physics behavior

**Trade-offs:**
- May slow down with many bodies
- CPU intensive (120 calculations/second)

**Best for:**
- Scientific accuracy (<50 bodies)
- Benchmarking
- Reproducible results
- Small simulations

### Comparison Table

| Feature | Adaptive | Precise |
|---------|----------|---------|
| Physics frequency | Variable (max 40 Hz) | Fixed (120 Hz) |
| Rendering FPS | Always 120 | May drop |
| CPU usage | Low | High |
| Accuracy | Medium | High |
| Deterministic | No | Yes |
| Max bodies (smooth) | ~400 | ~150 |
| Best for | Demos, exploration | Science, accuracy |

---

## Quick Start Guide

### First Launch

1. Run `src/gravity_engine.py` or `dist/GravityEngine.exe`
2. Wait for splash screen (3 seconds)
3. Click and hold to create a body (hold longer = larger)
4. Press P to generate random system (20 bodies)
5. Click a body to see detailed information
6. Press V to see vectors (red = velocity, blue = force)
7. Press Space to pause and analyze

### Creating Systems

**Binary System:**
1. Create two medium bodies (hold 2-3 seconds each)
2. Place close but not touching
3. Watch them orbit
4. Enable vectors (V) to see motion

**Chaotic Three-Body:**
1. Create three similar-sized bodies
2. Arrange in triangle
3. Press R for random mode
4. Add more bodies for chaos

**Central Star:**
1. Create one large central body (hold 5+ seconds)
2. Add smaller bodies around it
3. Disable fusion in config to prevent merging
4. Optional: Enable random mode for orbits

**Large Simulation (100+ bodies):**
1. Use adaptive mode (default)
2. Press P repeatedly (20 bodies each time)
3. Enjoy smooth 120 FPS
4. Watch the chaos!

---

## Troubleshooting

### Common Issues

**Font not found:**
- Ensure `assets/fonts/main_font.ttf` and `toruk.ttf` exist
- Check file paths are correct

**Simulation too fast/slow:**
- Adjust `self.time_acceleration` in config
- Default: 2e4 (20,000× real time)

**Poor performance:**
- Switch to adaptive mode
- Reduce physics frequency: `self.min_physics_interval = 0.050`
- Disable vectors (V key)
- Lower FPS: `self.FPS_TARGET = 60`

**Bodies pass through each other:**
- Fixed in v3.0.0 with visual collision detection
- Update to latest version
- Ensure `self.use_interpolation = True`

**Can't select bodies accurately:**
- Fixed in v3.0.0 with interpolated click detection
- Update to latest version

**Choppy vectors:**
- Fixed in v3.1.0 with complete interpolation
- Update to latest version
- Vectors now perfectly smooth

---

## Educational Use

Gravity Engine demonstrates:

1. **Newton's Law of Universal Gravitation** - F = G(m₁m₂)/r²
2. **Momentum Conservation** - Total momentum before = after
3. **Fixed Timestep Integration** - Deterministic physics
4. **Linear Interpolation** - Smooth rendering between states
5. **Adaptive Performance** - Throttling for user experience
6. **Kinetic Energy** - E = ½mv²
7. **Vector Mathematics** - Force and velocity decomposition
8. **N-body Problem** - Classical unsolved problem
9. **Visual Collision Detection** - Interpolated collision checking
10. **Numerical Stability** - Time accumulator, spiral prevention

Perfect for:
- Physics education (Newton's laws, gravity)
- Programming learning (game physics, Pygame, Python)
- Mathematics (vectors, trigonometry, integration)
- Computational thinking (optimization, algorithms)
- Performance optimization (adaptive systems)

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for complete development plans.

### Recently Completed (v3.1.0 - February 23, 2026)

- Complete Mode PRECISE interpolation (position, velocity, force, radius)
- Interpolation cache system
- 4 new unit tests for interpolation
- Perfectly smooth velocity and force vectors
- Progressive radius growth during fusions
- Comprehensive get_interpolated_state() method

### Recently Completed (v3.0.0 - February 19, 2026)

- Adaptive performance mode with throttling (40 Hz default)
- Visual collision detection on interpolated positions
- Interpolated click detection for selection
- Fixed timestep physics (1/120s)
- Time accumulator with spiral prevention
- Improved force vectors (logarithmic scaling)
- Testing framework (Tester class)

### Current Focus (March 2026)

| Priority | Feature | Status |
|----------|---------|--------|
| 1 | Scale factor system (pixel ≠ meter) | In Discussion |
| 2 | Unit system documentation (UNITS.md) | Planned |
| 3 | Adaptive interpolation (Hermite) | Planned |
| 4 | Partial mass transfer | Planned |
| 5 | QuadTree optimization | Planned |

### Next Milestones

- **March 2026**: Scale factor, adaptive interpolation, QuadTree
- **Q2 2026**: Save/load, UI improvements, camera system
- **Q3 2026**: Visual effects, analysis tools, documentation

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

- HIGH: Scale factor system (March 2026)
- MEDIUM: Adaptive interpolation (March 2026)
- MEDIUM: QuadTree optimization (March 2026)
- MEDIUM: Save/load system (May 2026)
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

*Last updated: February 23, 2026*  
*Version: 3.1.0 - Advanced Interpolation Edition*

---

*Enjoy exploring gravitational physics!*
