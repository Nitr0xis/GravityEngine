# Gravity Engine

A real-time N-body gravitational simulation built with Python and Pygame.

## Version 3.0.0 - Adaptive Performance Edition

**Created by [Nils DONTOT](https://github.com/Nitr0xis)**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)](https://www.pygame.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Nitr0xis-181717?logo=github)](https://github.com/Nitr0xis)

---

**Author:** Nils DONTOT  
**Repository:** [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)  
**Email:** [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)

---

## 📋 Table of Contents

- [Before We Begin](#-before-we-begin)
- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Building Executables](#-building-executables)
- [Controls](#-controls)
- [Configuration](#️-configuration)
- [Physics](#-physics)
- [Performance Modes](#-performance-modes)
- [Roadmap](#-roadmap)
- [Quick Start Guide](#-quick-start-guide)
- [Troubleshooting](#-troubleshooting)
- [Educational Use](#-educational-use)
- [Acknowledgments](#-acknowledgments)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🪶 Before We Begin

Hello, I am 15 years old and I am passionate about programming and physics. That is why I decided in mid-2025 to create a gravity simulator with Python. Here is the result of my work. Feel free to submit pull requests if you identify potential improvements or optimization opportunities. I am constantly trying to improve it, and I hope you like it.

Every previous change is available in [ROADMAP.md](ROADMAP.md).

## 🌌 Overview

Gravity Engine is an interactive physics simulation that allows you to create and observe celestial bodies interacting under Newtonian gravity. Watch bodies orbit, collide, and merge in real-time with adjustable parameters and visualization options.

The simulation features accurate Newtonian physics with momentum conservation, fixed timestep integration for determinism, smooth rendering with interpolation, and **adaptive performance mode** for smooth rendering on any hardware. Whether you want to recreate a solar system, observe chaotic three-body problems, or simply experiment with gravitational interactions, Gravity Engine provides an intuitive interface for exploration.

**Key Technical Features:**
- **Adaptive performance mode** - Intelligent throttling maintains smooth 120 FPS on any hardware
- **Visual collision detection** - Detects collisions on interpolated positions (what you see)
- **Fixed timestep physics** - Deterministic simulation regardless of rendering FPS
- **Interpolated rendering** - Smooth 120 FPS visuals even with variable frame rates
- **Time accumulator system** - Precise physics updates with "spiral of death" prevention
- **Momentum conservation** - Physically accurate collisions and mergers

**Developed by Nils DONTOT** - [GitHub Profile](https://github.com/Nitr0xis)

![Gravity Engine Demo](assets/demo.gif) *(A demo gif will soon be added)*

## ✨ Features

### Current Features (February 2026 - v3.0.0)
- ✅ **Adaptive performance mode** - Throttles physics calculations for smooth 120 FPS rendering
- ✅ **Visual collision detection** - Detects collisions on what you see (interpolated positions)
- ✅ **Smart click detection** - Select bodies based on their visual position, not physical
- ✅ **Real-time N-body simulation** - Accurate gravitational calculations for multiple bodies
- ✅ **Fixed timestep physics** - Deterministic simulation (1/120s physics steps)
- ✅ **Smooth interpolated rendering** - 120 FPS display with alpha blending between physics states
- ✅ **Time accumulator** - Handles variable frame rates while maintaining physics accuracy
- ✅ **Interactive body creation** - Click and hold to create bodies (exponential growth acceleration)
- ✅ **Momentum conservation** - Bodies merge realistically, conserving mass and momentum
- ✅ **Vector visualization** - Display velocity and force vectors in real-time (with interpolation)
- ✅ **Detailed analytics** - Track mass, velocity, energy, age, and more for each body
- ✅ **Pause/resume** - Freeze time to analyze your simulation
- ✅ **Random velocity mode** - Add chaos with randomized initial velocities
- ✅ **Reversed gravity** - Experiment with repulsive gravity (toggle with G key)
- ✅ **Fullscreen support** - Automatic native resolution detection
- ✅ **Random environments** - Generate preset configurations instantly (P key)
- ✅ **Standalone executable** - Build distributable .exe files (Windows)
- ✅ **Customizable splash screen** - Personalized startup screen with author info
- ✅ **Dark/Light mode** - Choose your preferred color scheme
- ✅ **Color class** - Organized color constants for easy customization
- ✅ **Tester class** - Unit tests for force summation, determinism, and uniform speed

### Recent Improvements (February 2026 - v3.0.0)
- 🔥 **NEW: Adaptive performance mode** - Physics throttled to max 40 Hz (configurable)
  - Smooth rendering even with 100+ bodies
  - Automatic CPU load management
  - Configurable update frequency (min_physics_interval)
- 🔥 **NEW: Visual collision detection** - Collisions detected on interpolated positions
  - No more "bodies passing through each other" visually
  - Instant physics calculation when visual collision occurs
  - Seamless integration with interpolation system
- 🔥 **NEW: Interpolated click detection** - Select bodies where you see them
  - Click detection uses visual positions, not physical positions
  - More intuitive user experience
  - Works perfectly with interpolation
- ✨ **Fixed timestep integration** - Physics now runs at consistent 1/120s intervals
- ✨ **Interpolation rendering** - Smooth visuals between physics steps (alpha blending)
- ✨ **Time accumulator** - Proper handling of variable frame rates
- ✨ **Interpolated vectors** - Velocity and force vectors now sync with interpolated positions
- ✨ **Improved force vectors** - Logarithmic scaling preserves direction and magnitude
- ✨ **Better cardinal vectors** - X/Y components properly interpolated
- ✨ **Code organization** - Color constants moved to dedicated `Color` class
- ✨ **Testing framework** - Added `Tester` class with physics validation tests

### Planned Features
See [ROADMAP.md](ROADMAP.md) for upcoming features and development timeline.

## 🚀 Installation

### Option 1: Use Pre-built Executable (Easiest)

**For Windows users:**

1. Download `GravityEngine.exe` from the [Releases](https://github.com/Nitr0xis/GravityEngine/releases) page
2. Double-click to run - no installation needed!

> 💡 **Note**: The executable is self-contained and includes all dependencies. No Python installation required.

### Option 2: Run from Source (For Developers)

**Prerequisites:**
- Python 3.11 or higher
- pip (Python package manager)

**Quick Start:**

1. **Clone the repository**
```bash
git clone https://github.com/Nitr0xis/GravityEngine.git
cd GravityEngine
```

2. **Install dependencies**
   
   The program will automatically install required dependencies on first run, or install manually:
```bash
pip install pygame
```

3. **Run the simulation**
```bash
python src/gravity_engine.py
```

### Option 3: Manual Installation with Virtual Environment
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install pygame

# Run the program
python src/gravity_engine.py
```

## 📁 Project Structure
```
GravityEngine/
│
├── dist/                           # 📦 Built executables (after building)
│   └── GravityEngine.exe          # Standalone executable (Windows)
│
├── src/
│   └── gravity_engine.py          # 🎯 Main program - run this to start
│
├── assets/
│   ├── fonts/
│   │   ├── main_font.ttf          # ✅ UI font (required)
│   │   └── toruk.ttf              # ✅ Splash screen font (required)
│   ├── icon.ico                   # 🎨 Executable icon
│   └── musics/                    # 🎵 Background music folder (optional)
│       ├── music1.mp3
│       ├── music2.mp3
│       └── music3.mp3
│
├── builders/                       # 🔨 Build scripts
│   ├── build.bat                  # Development build (with console)
│   ├── build_release.bat          # Release build (no console)
│   └── clean.bat                  # Clean build files
│
├── make.bat                        # 📋 Interactive build menu
├── README.md                       # 📖 This file
├── ROADMAP.md                      # 🗺️ Development roadmap
├── CONTRIBUTING.md                 # 🤝 How to contribute
├── SECURITY.md                     # 🔒 Security information
├── CODE_OF_CONDUCT.md              # 📜 Code of conduct
├── LICENSE                         # ⚖️ License terms (CC BY-NC-SA 4.0)
├── .gitignore                      # 🚫 Git ignore rules
└── .gitattributes                  # 📝 Git attributes
```

### Important Files

| File | Description | Required |
|------|-------------|----------|
| `dist/GravityEngine.exe` | Standalone executable (post-build) | 📦 Distributable |
| `src/gravity_engine.py` | Main Python source code | ✅ Required for dev |
| `assets/fonts/main_font.ttf` | UI font file | ✅ Required |
| `assets/fonts/toruk.ttf` | Splash screen font | ✅ Required |
| `assets/icon.ico` | Executable icon | 🎨 Recommended |
| `assets/musics/` | Background music files | 🎵 Optional |
| `builders/*.bat` | Build automation scripts | 🔨 For building |
| `make.bat` | Build system menu | 📋 Build interface |
| `README.md` | Documentation | 📖 You are here |
| `ROADMAP.md` | Development timeline | 🗺️ Recommended |
| `LICENSE` | License information | ⚖️ Legal |

## 🔨 Building Executables

### Using the Build Menu (Recommended)

Simply double-click `make.bat` to access the interactive build menu:
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

### Build Options Explained

| Option | Purpose | Output | Use Case |
|--------|---------|--------|----------|
| **[1] Development** | Quick build with debug console | `GravityEngine_Dev.exe` | Testing and debugging |
| **[2] Release** | Optimized build, no console | `GravityEngine.exe` | Distribution to users |
| **[3] Clean** | Remove all build artifacts | - | Fresh start |
| **[4] Clean + Build** | Clean, then release build | `GravityEngine.exe` | Final distribution |
| **[5] Run** | Launch Python source directly | - | Quick testing |
| **[6] Test Executable** | Run last built .exe | - | Verify build works |
| **[7] Open dist/** | Open folder in Explorer | - | View executables |
| **[8] Help** | Show detailed help | - | Learn about options |

### Build Requirements

- **PyInstaller** - Automatically installed on first build
- **All assets** - Must be present in `assets/` folder
- **Windows** - Build scripts are Windows batch files (.bat)

## 🎮 Controls

### Mouse Controls
- **Left Click** - Select a body / Create a new body (click on empty space)
- **Right Click** - Create a new body (hold to increase size)
- **Middle Click** - Create a new body (hold to increase size)
- **Hold Mouse Button** - Increase body size exponentially (growth accelerates over time)
- **Click on Body** - Select/deselect that specific body (uses visual position!)

### Keyboard Controls
| Key | Action |
|-----|--------|
| `Space` | Pause/unpause simulation |
| `V` | Toggle velocity vectors display |
| `R` | Toggle random velocity mode (randomizes initial velocities for new bodies) |
| `G` | Toggle reversed gravity (switch between attraction and repulsion) |
| `P` | Generate random environment (20 bodies by default) |
| `Delete` | Delete selected body |
| `Escape` | Exit program |

### Tips

- **Hold mouse button** to create larger bodies (size grows exponentially with time held)
- **Click quickly** to create small bodies
- **Select a body** to view detailed information (ID, mass, velocity, forces, age, etc.)
- **Use P key** to quickly populate the simulation with 20 random bodies
- **Pause with Space** to analyze the simulation state without time passing
- **Toggle vectors (V)** to visualize motion and forces (velocity in red, forces in blue)
- **Only one body can be selected at a time** - selecting a new body deselects the previous one
- **Click detection uses visual positions** - you can select bodies exactly where you see them

## ⚙️ Configuration

You can modify simulation parameters in the `Engine.__init__()` method within `src/gravity_engine.py`. Parameters are organized into logical sections:

### Splash Screen Settings
```python
self.splash_screen_font = Core.resource_path('assets/fonts/toruk.ttf')
self.splash_screen_enabled = True       # Enable/disable startup splash screen
self.splash_screen_duration = 3.0       # Duration in seconds
self.author_first_name = "Nils"         # Your first name
self.author_last_name = "DONTOT"        # Your last name
self.project_description = "Gravity Engine - A celestial body simulation"
```

### Display Settings
```python
self.FULLSCREEN = True                  # Enable fullscreen mode
self.screen_mode = "dark"               # Color scheme: "dark" or "light"
```

### Timestep Settings
```python
self.FPS_TARGET = 120                   # Target rendering FPS
self.physics_timestep = 1.0 / self.FPS_TARGET  # Fixed physics timestep (1/120s)
self.time_accumulator = 0.0             # Accumulator for physics updates
self.max_accumulation = 0.25            # Max accumulation (250ms = ~30 steps)
```

**Important**: The physics runs at a fixed timestep (1/120s) while rendering can vary. This ensures deterministic simulation.

### Simulation Settings
```python
self.FPS_TARGET = 120                   # Target frames per second
self.time_acceleration = 4e6            # Time acceleration factor
self.growing_speed = 0.1                # Base body growth rate when creating
```

### UI Settings
```python
self.used_font = Core.resource_path('assets/fonts/main_font.ttf')
self.txt_size = 30                      # Font size for UI text
self.txt_gap = 15                       # Spacing between text lines
self.info_y = 20                        # Y position for info display
```

### Physics Settings
```python
self.G = 6.6743e-11                     # Real gravitational constant (m³ kg⁻¹ s⁻²)
self.default_gravity = self.G           # Default gravity value
self.gravity = self.default_gravity     # Active gravitational constant
self.fusions = True                     # Enable/disable body fusion on collision
self.minimum_mass = 1e3                 # Minimum mass for new bodies (kg)
self.default_density = 5.514e3          # Default density (kg/m³) - Earth density
```

### Visualization Settings
```python
self.vectors_printed = False            # Show velocity vectors by default
self.force_vectors = True               # Show force vectors
self.cardinal_vectors = False           # Show X/Y velocity components separately
self.vectors_in_front = True            # Draw vectors on top of bodies
self.vector_scale = 1                   # Vector display scale multiplier
self.use_interpolation = True           # Enable smooth interpolation
```

### Performance Mode Settings (NEW in v3.0.0)
```python
self.performance_mode = "adaptive"      # "precise" or "adaptive"
# - "precise": Fixed timestep, deterministic, may slow with many bodies
# - "adaptive": Throttled updates, smooth rendering, less accurate

# Adaptive mode configuration
self.min_physics_interval = 0.025       # Min time between physics updates (25ms = 40 Hz)
self.last_physics_time = 0.0            # Timestamp of last physics calculation
self.physics_time_debt = 0.0            # Accumulated time since last calculation
```

**Performance modes explained:**

| Mode | Physics Frequency | Rendering | Accuracy | Use Case |
|------|------------------|-----------|----------|----------|
| **precise** | Fixed 120 Hz | May slow down | High | Small simulations (<50 bodies) |
| **adaptive** | Variable (max 40 Hz) | Always smooth | Medium | Large simulations (>50 bodies) |

### Random Generation Settings
```python
self.random_mode = False                # Random initial velocities on creation
self.random_environment_number = 20     # Bodies created with 'P' key

# Maximum kinetic energy for random velocities
max_kinetic_energy_joules = 1e-9        # in Joules
self.random_field = max_kinetic_energy_joules / (self.FPS_TARGET ** 2)
```

### Audio Settings
```python
self.musics_folder_path = "assets/musics"  # Music folder path
self.music = False                      # Enable/disable background music
self.music_volume = 1                   # Music volume (0.0 to 1.0)
```

### Quick Configuration Examples

#### High-Performance Mode (Large simulations)
```python
self.performance_mode = "adaptive"      # Enable adaptive throttling
self.min_physics_interval = 0.050       # Update every 50ms (20 Hz)
self.vectors_printed = False            # Disable vectors
self.force_vectors = False              # Disable force vectors
```

#### Maximum Accuracy Mode (Small simulations)
```python
self.performance_mode = "precise"       # Fixed timestep
self.FPS_TARGET = 120                   # High rendering FPS
self.vectors_printed = True             # Show all vectors
```

#### Chaotic System
```python
self.random_mode = True                 # Random initial velocities
max_kinetic_energy_joules = 5e-4        # Higher random energy
self.reversed_gravity = True            # Reverse gravity direction
self.fusions = False                    # Prevent merging for more chaos
```

#### Solar System-like Setup
```python
self.time_acceleration = 1e4            # Moderate time acceleration
self.fusions = False                    # Prevent planets from merging
self.random_mode = False                # Controlled initial conditions
self.performance_mode = "precise"       # High accuracy for orbits
```

## 🔬 Physics

### Fixed Timestep Integration

The simulation uses a **fixed timestep** system for deterministic physics:

```python
physics_timestep = 1.0 / 120  # Always 1/120 second per step
```

**How it works:**
1. **Time accumulator** collects real frame time
2. **Physics steps** execute when accumulator ≥ timestep
3. **Multiple steps** can run per frame if needed (catching up)
4. **Rendering interpolates** between physics states for smooth visuals

**Benefits:**
- ✅ **Deterministic** - Same initial conditions always give same results
- ✅ **FPS-independent** - Physics accuracy doesn't depend on rendering speed
- ✅ **Predictable** - No "time dilation" from slow frames
- ✅ **Smooth** - Interpolation provides fluid 120 FPS visuals

### Interpolated Rendering

Rendering uses **linear interpolation** (alpha blending) between physics states:

```python
# Alpha = progress between current and next physics step
alpha = time_accumulator / physics_timestep  # 0.0 to 1.0

# Interpolated position
render_x = prev_x + (x - prev_x) * alpha
render_y = prev_y + (y - prev_y) * alpha
```

**Result:** Smooth 120 FPS display even when physics runs at fixed intervals.

### Visual Collision Detection (NEW in v3.0.0)

Collisions are detected on **interpolated (visual) positions**, not just physical positions:

```python
# Check collision on what the user SEES
visual_x = prev_x + (x - prev_x) * alpha
visual_y = prev_y + (y - prev_y) * alpha

if visual_collision_detected:
    # Force immediate physics calculation
    physics_step(time_accumulator)
    # Save visual positions to avoid jumps
    prev_x = visual_x
    prev_y = visual_y
```

**Benefits:**
- ✅ No more bodies visually passing through each other
- ✅ Instant fusion when bodies appear to touch
- ✅ Seamless with interpolation system

### Gravitational Force

The simulation implements Newton's law of universal gravitation:
```
F = G × (m₁ × m₂) / r²
```

**Where:**
- `F` = gravitational force (Newtons)
- `G` = gravitational constant (6.6743 × 10⁻¹¹ m³ kg⁻¹ s⁻²)
- `m₁, m₂` = masses of the two bodies (kilograms)
- `r` = distance between body centers (meters)

**Implementation:**
```python
force = engine.gravity * ((self.mass * other.mass) / (distance ** 2))
angle = atan2(dy, dx)
fx = cos(angle) * force
fy = sin(angle) * force
```

### Velocity Updates

Forces are applied to velocity each physics step:
```python
# In attract() method
self.vx += fx / self.mass  # a = F/m
self.vy += fy / self.mass
```

### Position Updates

Position is updated with time acceleration:
```python
# In physics_update() method
dt_sim = dt * engine.time_acceleration
self.x += self.vx * dt_sim
self.y += self.vy * dt_sim
```

### Momentum Conservation

All interactions conserve momentum:
```
p_total = m₁v₁ + m₂v₂ = constant
```

**Fusion example:**
```python
# New velocity after fusion
v_new = (m₁ × v₁ + m₂ × v₂) / (m₁ + m₂)
```

### Body Fusion

When two bodies collide (distance ≤ sum of radii):

**Conservation laws:**
- **Mass**: `m_new = m₁ + m₂`
- **Position (center of mass)**: `x_new = (m₁x₁ + m₂x₂) / m_total`
- **Velocity (momentum)**: `v_new = (m₁v₁ + m₂v₂) / m_total`

**New radius:**
```python
volume = mass / density
radius = ((3 × volume) / (4π))^(1/3)
```

### Force Vector Visualization

Force vectors use **logarithmic scaling** with **direction preservation**:

```python
# Calculate unit vector (preserves direction)
force_magnitude = sqrt(fx² + fy²)
unit_x = fx / force_magnitude
unit_y = fy / force_magnitude

# Logarithmic scaling for visibility
visual_length = log10(force_magnitude + 1) × scale_factors

# Final vector
vector_x = unit_x × visual_length
vector_y = unit_y × visual_length
```

**Benefits:**
- ✅ Direction is **always correct** (no sign loss)
- ✅ Large forces are compressed (logarithmic)
- ✅ Small forces remain visible

### Units

| Property | Unit | Symbol | Notes |
|----------|------|--------|-------|
| Mass | Kilograms | kg | Base unit |
| Distance | Meters | m | Screen pixels represent meters |
| Time | Seconds | s | Accelerated by `time_acceleration` |
| Force | Newtons | N | F = ma |
| Velocity | Meters/second | m/s | Magnitude of velocity vector |
| Density | kg/m³ | - | Default: 5514 (Earth) |

### Testing Framework

The `Tester` class includes unit tests:

```python
Tester.test_force_summation()    # Verify forces are summed correctly
Tester.test_determinism()        # Verify same inputs → same outputs
Tester.test_uniform_speed()      # Verify FPS-independent physics
```

## 🎯 Performance Modes

### Adaptive Mode (NEW in v3.0.0) - Default

**How it works:**
- Physics calculations are **throttled** to a maximum frequency
- Default: 40 Hz (1 calculation every 25ms)
- Rendering stays at smooth 120 FPS via interpolation
- Automatically adapts to CPU load

**Configuration:**
```python
self.performance_mode = "adaptive"
self.min_physics_interval = 0.025  # 25ms = 40 Hz physics
```

**Example timeline:**
```
Frame 1 (t=0ms):    Physics calculation (dt=0ms)
Frame 2 (t=8ms):    Skip physics, render interpolated
Frame 3 (t=16ms):   Skip physics, render interpolated
Frame 4 (t=25ms):   Physics calculation (dt=25ms)
Frame 5 (t=33ms):   Skip physics, render interpolated
...
```

**Benefits:**
- ✅ **Always smooth rendering** - 120 FPS regardless of body count
- ✅ **CPU efficient** - Max 40 physics calculations/second
- ✅ **Scalable** - Handle 100+ bodies smoothly
- ✅ **Configurable** - Adjust min_physics_interval

**Trade-offs:**
- ⚠️ **Lower accuracy** - Large timesteps (25ms vs 8.3ms)
- ⚠️ **Non-deterministic** - Results vary slightly on different hardware
- ⚠️ **May miss fast collisions** - Rare with visual collision detection

**Best for:**
- Large simulations (>50 bodies)
- Smooth demonstrations
- Low-end hardware
- Visual exploration

### Precise Mode

**How it works:**
- Fixed timestep: exactly 1/120 second per physics step
- May do multiple physics steps per frame to catch up
- Slows down visually if CPU can't keep up

**Configuration:**
```python
self.performance_mode = "precise"
```

**Benefits:**
- ✅ **High accuracy** - Small timesteps (8.3ms)
- ✅ **Deterministic** - Same results every run
- ✅ **Predictable** - Consistent physics behavior

**Trade-offs:**
- ⚠️ **May slow down** - Visual slowdown with many bodies
- ⚠️ **CPU intensive** - 120 calculations/second

**Best for:**
- Scientific accuracy
- Small simulations (<50 bodies)
- Benchmarking
- Reproducible results

### Comparison Table

| Feature | Adaptive Mode | Precise Mode |
|---------|---------------|--------------|
| Physics frequency | Variable (max 40 Hz) | Fixed (120 Hz) |
| Rendering FPS | Always 120 | May drop below 120 |
| CPU usage | Low | High |
| Accuracy | Medium | High |
| Deterministic | No | Yes |
| Max bodies (smooth) | 100+ | ~50 |
| Visual collision | ✅ Yes | ✅ Yes |
| Best for | Demos, exploration | Science, accuracy |

### Choosing the Right Mode

**Use Adaptive Mode if:**
- You have >50 bodies
- Smooth rendering is priority
- Running on older hardware
- Demonstrating concepts visually

**Use Precise Mode if:**
- You need reproducible results
- Scientific accuracy is critical
- You have <50 bodies
- Benchmarking performance

### Adjusting Adaptive Mode

You can fine-tune the physics update frequency:

```python
# Ultra-smooth (20 Hz physics)
self.min_physics_interval = 0.050  # 50ms between updates

# Balanced (40 Hz physics) - Default
self.min_physics_interval = 0.025  # 25ms between updates

# Higher accuracy (60 Hz physics)
self.min_physics_interval = 0.017  # ~17ms between updates

# Very high accuracy (100 Hz physics)
self.min_physics_interval = 0.010  # 10ms between updates
```

**Rule of thumb:** Higher frequency = more accurate but more CPU intensive.

## 📊 Performance

### Current Performance

- **Algorithm**: O(n²) brute-force gravitational calculations
- **Rendering**: Interpolated 120 FPS
- **Physics (adaptive)**: Max 40 Hz (configurable)
- **Physics (precise)**: Fixed 120 Hz
- **Memory**: ~50-100 MB typical usage

### Performance Characteristics

**Adaptive mode characteristics:**
- ✅ Smooth 120 FPS with 100+ bodies
- ✅ Automatic CPU load management
- ✅ Visual collision detection prevents tunneling
- ⚠️ Reduced physics accuracy with large timesteps

**Precise mode characteristics:**
- ✅ Consistent physics regardless of rendering FPS
- ✅ Deterministic simulation (same inputs → same outputs)
- ✅ No "time dilation" from slow frames
- ⚠️ May slow down visually with many bodies

### Performance Tips

1. **Use adaptive mode** - For large simulations (>50 bodies)
2. **Reduce body count** - Fewer bodies = dramatically faster (O(n²) complexity)
3. **Disable vectors** - Turn off visualization (V key)
4. **Adjust physics frequency** - Lower min_physics_interval for better performance
5. **Lower FPS target** - `self.FPS_TARGET = 60` instead of 120
6. **Disable force vectors** - `self.force_vectors = False`
7. **Adjust time acceleration** - Higher values = faster evolution

### Benchmarks (Approximate)

**Adaptive Mode (min_physics_interval = 0.025s):**

| Bodies | Visual FPS | Physics Hz | Smooth? |
|--------|-----------|------------|---------|
| 10 | 120 | 40 | ✅ Yes |
| 50 | 120 | 40 | ✅ Yes |
| 100 | 90 | 40 | ✅ Yes |
| 200 | 70 | 30-40 | ✅ Yes |
| 500+ | 20-40 | 20-30 | ⚠️ Mostly |

**Precise Mode (physics_timestep = 1/120s):**

| Bodies | FPS (120 target) | Physics Steps/Frame |
|--------|------------------|---------------------|
| 10 | 90-120 | 1 |
| 50 | 70-90 | 1 |
| 100 | 50-70 | 1-2 |
| 200 | 10-20 | 2-3 |
| 500+ | <10 | 5+ |

> 💡 Adaptive mode maintains smooth rendering regardless of body count.

## 📈 Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plans and timelines.

### Recently Completed (February 2026 - v3.0.0)

- ✅ Adaptive performance mode with throttling
- ✅ Visual collision detection on interpolated positions
- ✅ Interpolated click detection for body selection
- ✅ Fixed timestep physics integration
- ✅ Interpolated rendering system
- ✅ Time accumulator with spiral-of-death prevention
- ✅ Improved force vector visualization (logarithmic scaling)
- ✅ Interpolated vector rendering
- ✅ Color class organization
- ✅ Testing framework (Tester class)
- ✅ Multiple font support (main UI + splash screen)

### Current Development Focus

| Priority | Feature | Status |
|----------|---------|--------|
| 1 | Scale factor system (pixel ≠ meter) | 🔄 In Discussion |
| 2 | Unit system coherence | ⏳ In Progress |
| 3 | Partial mass transfer on collision | 📋 Planned |
| 4 | QuadTree optimization | 📋 Planned |

### Next Milestones

- **February-March 2026**: Scale factor implementation, unit system finalization
- **March 2026**: Partial collisions, QuadTree optimization
- **Q2 2026**: Save/load system, UI improvements, configuration files

## 🎯 Quick Start Guide

### First Launch

1. **Run** `src/gravity_engine.py` or `dist/GravityEngine.exe`
2. **Wait** for splash screen (3 seconds, shows author info)
3. **Click and hold** anywhere to create a body (hold longer = larger body)
4. **Release** to place it
5. **Press P** to generate a random system (20 bodies)
6. **Click a body** to see its detailed information
7. **Press V** to see velocity vectors (red) and force vectors (blue)
8. **Press Space** to pause and analyze

### Creating Interesting Systems

**Simple Binary System:**
1. Create two medium-sized bodies (hold for ~2-3 seconds each)
2. Place them close together (but not touching)
3. Watch them orbit each other!
4. Enable vectors (V) to see their motion

**Chaotic Three-Body:**
1. Create three bodies of similar size
2. Arrange in a triangle pattern
3. Press R to enable random mode
4. Create more bodies to see chaotic interactions

**Central Star with Planets:**
1. Create one very large central body (hold for 5+ seconds)
2. Add several smaller bodies around it
3. Disable fusion (`self.fusions = False` in config) to prevent merging
4. Optionally enable random mode for orbital velocities

**Large-Scale Simulation (100+ bodies):**
1. Switch to adaptive mode (`self.performance_mode = "adaptive"`)
2. Press P repeatedly to add 20 bodies at a time
3. Enjoy smooth 120 FPS rendering even with 100+ bodies
4. Watch the chaos unfold!

### Understanding the Display

**Main Info Panel (Top Left):**
- Number of bodies
- Total mass in system
- Heaviest body ID and mass
- Oldest body ID and age

**Selected Body Panel (Left Side):**
- Body ID and age (simulated years)
- Mass (kg), Radius (m), Volume (m³), Density (kg/m³)
- Kinetic energy (J)
- Force applied (N)
- Velocity (m/s)
- Coordinates (x, y)
- Nearest body and distance

**Top Right:**
- Reversed gravity status
- Vectors display status
- Random mode status
- Random environment info (P key)

**Bottom:**
- Simulation age (years)
- Current FPS (rendering)
- Time acceleration factor
- Pause status

## 🔧 Troubleshooting

### Common Issues

**Problem**: Font not found / Text doesn't display
- **Solution**: Ensure `assets/fonts/main_font.ttf` and `assets/fonts/toruk.ttf` exist
- Check file paths are correct
- In PyInstaller builds, fonts must be in `assets/fonts/` folder

**Problem**: Simulation runs too fast/slow
- **Solution**: Adjust `self.time_acceleration` in `Engine.__init__()`
- Default: `4e6` (4 million × real time)
- Lower = slower simulation, Higher = faster simulation

**Problem**: Poor performance with many bodies
- **Solution**: 
  - Switch to adaptive mode: `self.performance_mode = "adaptive"`
  - Reduce physics frequency: `self.min_physics_interval = 0.050` (20 Hz)
  - Disable vectors (V key)
  - Lower FPS target: `self.FPS_TARGET = 60`
  - Disable force vectors: `self.force_vectors = False`

**Problem**: Bodies pass through each other visually
- **Solution**: This was fixed in v3.0.0 with visual collision detection
- Update to latest version if using older code
- Ensure `self.use_interpolation = True`

**Problem**: Can't select bodies accurately
- **Solution**: This was fixed in v3.0.0 with interpolated click detection
- Update to latest version
- Click detection now uses visual positions

**Problem**: Physics changes with different FPS
- **Solution**: This was fixed with fixed timestep integration
- Physics now runs at consistent intervals regardless of rendering FPS

**Problem**: Choppy rendering in adaptive mode
- **Solution**: 
  - Reduce min_physics_interval for more frequent updates
  - Check if too many bodies (>200)
  - Disable vectors to reduce rendering load

## 🎓 Educational Use

Gravity Engine is perfect for:

- **Physics education** - Demonstrate Newton's laws and gravitational concepts
- **Programming learning** - Study game physics, Pygame, and Python
- **Scientific visualization** - Explore N-body problems and chaos theory
- **Mathematics** - Understand vectors, trigonometry, and numerical integration
- **Computational thinking** - Learn about optimization and algorithms
- **Performance optimization** - Study adaptive systems and throttling

### Educational Topics Demonstrated

1. **Newton's Law of Universal Gravitation** - F = G(m₁m₂)/r²
2. **Momentum Conservation** - Total momentum before = after
3. **Fixed Timestep Integration** - Deterministic physics simulation
4. **Interpolation** - Smooth rendering between discrete states
5. **Adaptive Performance** - Throttling for smooth user experience
6. **Numerical Stability** - Time accumulator and spiral-of-death prevention
7. **Kinetic Energy** - E = ½mv²
8. **Vector Mathematics** - Force and velocity decomposition
9. **N-body Problem** - Classical unsolved problem in physics
10. **Visual Collision Detection** - Detecting collisions on interpolated positions

## 🙏 Acknowledgments

- **Pygame** - Amazing game development library ([pygame.org](https://www.pygame.org/))
- **PyInstaller** - Executable building tool
- **Newton** - For the physics (obviously! 😄)
- **Python Community** - For excellent documentation and support
- **Glenn Fiedler** - For excellent articles on fixed timestep game loops
- **You** - For checking out this project!

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **Report bugs** - Open an issue with detailed description
2. **Suggest features** - Share your ideas in issues
3. **Submit pull requests** - Fix bugs or add features
4. **Improve documentation** - Help make the README clearer
5. **Share your simulations** - Show what you've created!
6. **Optimize code** - Help improve performance

### Development Workflow
```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/GravityEngine.git
cd GravityEngine

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes
# Edit src/gravity_engine.py

# 4. Test thoroughly
python src/gravity_engine.py

# 5. Commit and push
git add .
git commit -m "Add: description of changes"
git push origin feature/your-feature-name

# 6. Create pull request on GitHub
```

### Code Style Guidelines

- **Follow PEP 8** - Python style guide
- **Add docstrings** - Document classes and methods
- **Comment physics** - Explain formulas and calculations
- **Test thoroughly** - Verify physics accuracy
- **Use type hints** - Add type annotations

### Areas Needing Help

- 🐛 **Bug fixes** - Physics edge cases, UI issues
- ⚡ **Performance** - QuadTree, spatial partitioning
- 📊 **Physics** - Scale factor, unit consistency
- 🎨 **UI/UX** - Better visualization, settings menu
- 📖 **Documentation** - Tutorials, examples
- 🧪 **Testing** - More unit tests, physics validation

## 📝 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**.

[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Copyright © 2026 Nils DONTOT**

### You are free to:

- ✅ **Share** - Copy and redistribute
- ✅ **Adapt** - Remix, transform, build upon

### Under the following terms:

- 📛 **Attribution** - Give credit to Nils DONTOT
- 🚫 **NonCommercial** - No commercial use
- 🔄 **ShareAlike** - Distribute under same license

See [LICENSE](LICENSE) for complete terms.

## 📧 Contact

**Nils DONTOT**

- 📧 **Email**: [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)
- 🐙 **GitHub**: [@Nitr0xis](https://github.com/Nitr0xis)
- 🔗 **Repository**: [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)
- 🌐 **Issues**: [Report bugs or suggest features](https://github.com/Nitr0xis/GravityEngine/issues)

---

**⭐ Star this repository if you find it interesting!**

**Made with ❤️ and ☕ by [Nils DONTOT](https://github.com/Nitr0xis) (age 15)**

*Last updated: February 19, 2026*  
*Version: 3.0.0 - Adaptive Performance Edition*

---

*Enjoy exploring the cosmos! 🌌*
