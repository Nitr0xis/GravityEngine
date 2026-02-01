# Gravity Engine

A real-time N-body gravitational simulation built with Python and Pygame.

**Created by [Nils DONTOT](https://github.com/Nitr0xis)**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
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
- [Performance](#-performance)
- [Roadmap](#-roadmap)
- [Screenshots](#-screenshots)
- [Educational Use](#-educational-use)
- [Quick Start Guide](#-quick-start-guide)
- [Troubleshooting](#-troubleshooting)
- [Additional Resources](#-additional-resources)
- [Color Scheme Reference](#-color-scheme-reference)
- [Acknowledgments](#-acknowledgments)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🪶 Before We Begin

Hello, I am 15 years old and I am passionate about programming and physics. That is why I decided in mid-2025 to create a gravity simulator with Python. Here is the result of my work. Feel free to submit pull requests if you identify potential improvements or optimization opportunities. I am constantly trying to improve it, and I hope you like it.

Every previous change is available in [ROADMAP.md](ROADMAP.md).

## 🌌 Overview

Gravity Engine is an interactive physics simulation that allows you to create and observe celestial bodies interacting under Newtonian gravity. Watch bodies orbit, collide, and merge in real-time with adjustable parameters and visualization options.

The simulation features accurate Newtonian physics with momentum conservation, customizable gravitational constants, and multiple visualization modes. Whether you want to recreate a solar system, observe chaotic three-body problems, or simply experiment with gravitational interactions, Gravity Engine provides an intuitive interface for exploration.

**Developed by Nils DONTOT** - [GitHub Profile](https://github.com/Nitr0xis)

![Gravity Engine Demo](assets/demo.gif) *(A demo gif will soon be added)*

## ✨ Features

### Current Features
- ✅ **Real-time N-body simulation** - Accurate gravitational calculations for multiple bodies
- ✅ **Interactive body creation** - Click and hold to create bodies of any size (with exponential growth acceleration)
- ✅ **Momentum conservation** - Bodies merge realistically, conserving mass and momentum
- ✅ **Vector visualization** - Display velocity and force vectors in real-time
- ✅ **Detailed analytics** - Track mass, velocity, energy, age, and more for each body
- ✅ **Pause/resume** - Freeze time to analyze your simulation
- ✅ **Random velocity mode** - Add chaos with randomized initial velocities
- ✅ **Reversed gravity** - Experiment with repulsive gravity (toggle with G key)
- ✅ **FPS correction** - Consistent physics regardless of frame rate
- ✅ **Fullscreen support** - Automatic native resolution detection
- ✅ **Random environments** - Generate preset configurations instantly (P key)
- ✅ **Standalone executable** - Build distributable .exe files (Windows)
- ✅ **Customizable splash screen** - Personalized startup screen with author info
- ✅ **Dark/Light mode** - Choose your preferred color scheme
- ✅ **Cardinal vector display** - Show X and Y velocity components separately

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
- Python 3.8 or higher
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
│   ├── font.ttf                   # ✅ UI font (required)
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
├── CONTRIBUTING.md                 # 🗺️ How to contribute
├── SECURITY.md                     # 🗺️ About the security risks of the project
├── CODE_OF_CONDUCT                 # 🗺️ Code of conduct
├── LICENSE                         # ⚖️ License terms (CC BY-NC-SA 4.0)
├── .gitignore                      # 🚫 Git ignore rules
└── .gitattributes                  # 📝 Git attributes
```

### Important Files

| File | Description | Required |
|------|-------------|----------|
| `dist/GravityEngine.exe` | Standalone executable (post-build) | 📦 Distributable |
| `src/gravity_engine.py` | Main Python source code | ✅ Required for dev |
| `assets/font.ttf` | UI font file | ✅ Required |
| `assets/icon.ico` | Executable icon | 🎨 Recommended |
| `assets/musics/` | Background music files | 🎵 Optional |
| `builders/*.bat` | Build automation scripts | 🔨 For building |
| `make.bat` | Build system menu | 📋 Build interface |
| `README.md` | Documentation | 📖 Recommended |
| `ROADMAP.md` | Development timeline | 🗺️ Recommended |
| `LICENSE` | License information | ⚖️ Legal |

### The `dist/` Folder

The `dist/` folder contains built executables created by PyInstaller:

- **Created by**: Running `build.bat` or `build_release.bat`
- **Contents**: Self-contained `.exe` files with all dependencies embedded
- **Distribution**: Share `GravityEngine.exe` with users who don't have Python
- **Size**: Approximately 15-30 MB (includes Python runtime, Pygame, and assets)
- **Ignored by Git**: Not tracked in version control (too large)

> 💡 **Tip**: Users who download your executable don't need Python, Pygame, or any dependencies installed!

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

### Manual Building

**Development Build (with console for debugging):**
```bash
builders\build.bat
```

**Release Build (no console, for distribution):**
```bash
builders\build_release.bat
```

**Clean build files:**
```bash
builders\clean.bat
```

### Build Requirements

- **PyInstaller** - Automatically installed on first build
- **All assets** - Must be present in `assets/` folder
- **Windows** - Build scripts are Windows batch files (.bat)

> 💡 **Note**: On first build, PyInstaller will be automatically installed if not present.

### Distributing Your Build

After building, share **only** the `dist/GravityEngine.exe` file:

1. Build release version: `make.bat` → Option `[2]`
2. Find executable in `dist/GravityEngine.exe`
3. Share this single file - it contains everything!
4. Users double-click to run - no installation needed

## 🎮 Controls

### Mouse Controls
- **Left Click** - Select a body / Create a new body (click on empty space)
- **Right Click** - Create a new body (hold to increase size)
- **Middle Click** - Create a new body (hold to increase size)
- **Hold Mouse Button** - Increase body size exponentially (growth accelerates over time)
- **Click on Body** - Select/deselect that specific body

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

## ⚙️ Configuration

You can modify simulation parameters in the `Engine.__init__()` method within `src/gravity_engine.py`. Parameters are organized into logical sections:

### Splash Screen Settings
```python
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

### UI Settings
```python
self.txt_size = 30                      # Font size for UI text
self.txt_gap = 15                       # Spacing between text lines
self.info_y = 20                        # Y position for info display
self.used_font = resource_path('assets/font.ttf')  # Font file path
```

### Physics Settings
```python
self.G = 6.6743e-11                     # Real gravitational constant (m³ kg⁻¹ s⁻²)
self.default_gravity = self.G           # Default gravity value
self.gravity = self.default_gravity     # Active gravitational constant
self.fusions = True                     # Enable/disable body fusion on collision
self.minimum_mass = 1000                # Minimum mass for new bodies (kg)
```

### Simulation Settings
```python
self.FPS = 120                          # Target frames per second
self.time_acceleration = 50_000                     # Time acceleration factor
self.growing_speed = 0.1                # Base body growth rate when creating
```

**Important**: The body growth uses exponential acceleration - the longer you hold the mouse button, the faster the body grows. The acceleration formula is:
```python
acceleration_factor = exp(time_held * 0.8)
```

### Density Settings
```python
self.default_density = 5515             # Default density for new bodies (kg/m³)
                                        # 5515 is Earth's average density
```

The radius is calculated from mass and density using:
```python
volume = mass / density
radius = ((3 * volume) / (4 * π))^(1/3)
```

### Visualization Settings
```python
self.vectors_printed = False            # Show velocity vectors by default
self.strength_vectors = True            # Show force vectors
self.cardinal_vectors = False           # Show X/Y velocity components separately
self.vectors_in_front = True            # Draw vectors on top of bodies
self.vector_length = 1                  # Vector display scale multiplier
```

**Vector Colors:**
- **Red (GSV)**: Global Speed Vector - total velocity
- **Green (CSV_x)**: Cardinal Speed Vector X - horizontal component
- **Yellow (CSV_y)**: Cardinal Speed Vector Y - vertical component
- **Special Blue**: Force vectors

### Random Generation Settings
```python
self.random_mode = False                # Random initial velocities on creation
self.random_environment_number = 20     # Bodies created with 'P' key

# Maximum kinetic energy for random velocities
max_kinetic_energy_joules = 5e-5        # in Joules
# Converted to simulation units (kg⋅m²/frame²)
self.random_field = max_kinetic_energy_joules / (self.FPS ** 2)
```

When random mode is enabled, new bodies receive random velocities based on:
```python
max_velocity = sqrt(2 * random_field / mass)
vx = random.uniform(-max_velocity, max_velocity)
vy = random.uniform(-max_velocity, max_velocity)
```

### Audio Settings
```python
self.musics_folder_path = resource_path('assets/musics')
self.music = False                      # Enable/disable background music
self.music_volume = 1                   # Music volume (0.0 to 1.0)
```

**Music Queue**: The simulation can play up to 3 music files in sequence:
- `music1.mp3`
- `music2.mp3`
- `music3.mp3`

Place these files in `assets/musics/` to enable background music.

### Quick Configuration Examples

#### Slower, More Visible Simulation
```python
self.time_acceleration = 1_000          # Reduce time acceleration dramatically
self.vectors_printed = True             # Show vectors by default
self.vector_length = 2                  # Make vectors longer
self.cardinal_vectors = True            # Show X/Y components
```

#### High-Performance Mode
```python
self.FPS = 60                           # Lower FPS for better performance
self.vectors_printed = False            # Disable vectors
self.strength_vectors = False           # Disable force vectors
self.vectors_in_front = False           # Skip vector layer
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
self.time_acceleration = 10_000         # Moderate time acceleration
self.fusions = False                    # Prevent planets from merging
self.random_mode = False                # Controlled initial conditions
self.default_density = 5515             # Earth-like density
```

#### Fast Body Creation
```python
self.growing_speed = 0.5                # Faster base growth
self.minimum_mass = 100                 # Smaller minimum mass
```

### Advanced Configuration

For more advanced modifications, you can edit:

- **Body creation behavior** → `Circle.__init__()`
- **Force calculations** → `Circle.attract()`
- **Collision & fusion** → `Circle.fusion()` and `Circle.update_fusion()`
- **Keyboard mappings** → `Engine.run()` → `KEY_MAP`
- **Mouse actions** → `ActionManager.handle_mouse_button_down()` and `handle_mouse_button_up()`
- **Growth acceleration** → `Engine.run()` main loop (search for "acceleration_factor")

### Configuration File *(Future Feature)*

> 📋 **Coming Q2 2026**: External configuration file support (JSON/YAML). See [ROADMAP.md](ROADMAP.md).

## 🔬 Physics

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

**Implementation Details:**
- Force is decomposed into X and Y components using trigonometry
- Angle is calculated as: `angle = atan2(dy, dx)`
- Components: `fx = cos(angle) * force`, `fy = sin(angle) * force`
- If reversed gravity is enabled, forces are multiplied by -1

### Velocity Updates

Forces are applied to velocity using:
```python
vx += fx / mass  # Acceleration = Force / Mass
vy += fy / mass
```

Position is updated with frame-rate correction:
```python
x += correct_latency(vx * speed)
y += correct_latency(vy * speed)
```

Where `correct_latency()` adjusts for actual FPS:
```python
final_speed = speed * 100 * (1 / frequency)
```

### Momentum Conservation

All interactions conserve momentum using:
```
p_total = m₁v₁ + m₂v₂ = constant
```

This ensures physically accurate collisions and mergers.

### Body Fusion

When two bodies collide (distance ≤ sum of radii), they merge while conserving:

**Conditions for fusion:**
- `fusions` must be enabled
- The calling body must have mass ≥ the other body
- Distance between centers ≤ radius of larger body

**Conservation laws:**
- **Mass**: `m_new = m₁ + m₂`
- **Position (center of mass)**: `x_new = (m₁x₁ + m₂x₂) / m_total`
- **Velocity (momentum conservation)**: `v_new = (m₁v₁ + m₂v₂) / m_total`

**New radius calculation:**
```python
if density > 0:
    volume = mass / density
    radius = ((3 * volume) / (4 * π))^(1/3)
else:
    radius = mass^(1/3)  # Fallback
```

The absorbed body is marked with `suicide = True` and removed in the next frame.

### Force Averaging (Important Note)

⚠️ **Current implementation**: Forces from all bodies are **averaged** rather than summed:
```python
self.force[0] /= len(self.attract_forces)
self.force[1] /= len(self.attract_forces)
```

This is unusual for physics simulations (forces should typically be summed). This might be an intentional design choice or could be modified for more standard physics.

### Time Acceleration

The simulation includes a configurable time acceleration factor (`self.time_acceleration`):
- Default: 50,000× real-time
- Real-time physics calculations
- FPS-independent updates ensure consistent physics
- Position updates scaled by: `time_acceleration * 100 * (1 / frequency)`

### Kinetic Energy

Kinetic energy is calculated as:
```python
E = 0.5 * mass * velocity²
```

Where velocity is the magnitude: `sqrt(vx² + vy²) * FPS`

### Units

| Property | Unit | Symbol | Notes |
|----------|------|--------|-------|
| Mass | Kilograms | kg | Base unit |
| Distance | Meters | m | Screen pixels represent meters |
| Radius | Meters | m | Calculated from mass and density |
| Time | Seconds | s | Accelerated by `speed` factor |
| Force | Newtons | N | F = ma |
| Energy | Joules | J | E = 0.5mv² |
| Velocity | Meters/second | m/s | Magnitude of velocity vector |
| Density | kg/m³ | - | Default: 5515 (Earth) |
| Age | Seconds → Years | - | Displayed after conversion |

**Age Display Conversion:**
```python
age_years = age_seconds * speed / 31_557_600
# 31,557,600 = seconds in a year
```

> ⚠️ **Note**: The current implementation mixes simulation units and real-world units. A unit system revision is planned. See [ROADMAP.md](ROADMAP.md).

### Known Physics Quirks

1. **Force Averaging**: Forces are averaged instead of summed (see above)
2. **Displayed Force Scaling**: Display forces are converted with `f_display = f_sim / gravity * G`
3. **Mixed Units**: Some calculations mix pixels with meters

These will be addressed in future updates (see ROADMAP.md for "Coherent physical units" milestone).

## 📊 Performance

### Current Performance

- **Algorithm**: O(n²) brute-force gravitational calculations
- **Optimal range**: Up to ~50-100 bodies at 120 FPS (depends on hardware)
- **FPS independence**: Physics accuracy maintained regardless of frame rate
- **Memory**: ~50-100 MB typical usage
- **Frame rate correction**: Automatic latency compensation ensures consistent simulation

### Performance Characteristics

**What affects performance:**
- **Body count** - Quadratic scaling (O(n²))
- **Vector rendering** - Each vector is drawn separately
- **Force calculations** - All pairs calculated every frame
- **Selection checks** - Distance calculations for mouse clicks
- **Screen resolution** - Higher resolution = more pixels to render

**What doesn't affect performance:**
- Time acceleration (`speed` parameter)
- Body size (radius)
- Pause state (no physics updates when paused)

### Performance Tips

1. **Reduce body count** - Fewer bodies = dramatically faster (O(n²) complexity)
2. **Disable vectors** - Turn off visualization for better performance (V key)
3. **Lower FPS** - `self.FPS = 60` instead of 120 is often sufficient
4. **Disable force vectors** - `self.strength_vectors = False`
5. **Windowed mode** - Slightly faster than fullscreen on some systems
6. **Close other applications** - Free up system resources

### Bottlenecks

**Current performance bottlenecks:**
1. **Nested loops** - Every body calculates force with every other body
2. **No spatial partitioning** - All distances calculated regardless of proximity
3. **Single-threaded** - No parallelization of force calculations
4. **Vector rendering** - Each vector drawn individually

### Benchmarks (Approximate)

| Bodies | FPS (120 target) | FPS (60 target) |
|--------|------------------|-----------------|
| 10 | 120 | 60 |
| 50 | 100-120 | 60 |
| 100 | 60-80 | 50-60 |
| 200 | 30-40 | 30-40 |
| 500+ | <20 | <20 |

> 💡 These are estimates and vary significantly based on hardware (CPU speed, RAM, graphics).

### Planned Optimizations

See [ROADMAP.md](ROADMAP.md) for upcoming performance improvements:

- **QuadTree/Barnes-Hut** - Reduce complexity to O(n log n)
- **Spatial partitioning** - Only calculate forces for nearby bodies
- **Multi-threading** - Parallel force calculations
- **GPU acceleration** - CUDA support for thousands of bodies
- **Cached calculations** - Store and reuse distance calculations
- **Collision optimization** - Efficient broad-phase detection

## 📈 Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plans and timelines.
Previous features and completed milestones are documented in the file.

### Current Development Focus

| Priority | Feature | Status |
|----------|---------|--------|
| 1 | Coherent physical units | ⏳ In Progress |
| 2 | Screen-relative display system | ⏳ In Progress |
| 3 | Partial mass transfer on collision | 📋 Planned |
| 4 | QuadTree optimization | 📋 Planned |

### Next Milestones

- **February 2026**: Unit system overhaul, screen-relative display
- **March 2026**: Partial collisions, QuadTree optimization
- **Q2 2026**: Save/load system, UI improvements, configuration files

### Recently Completed

- ✅ Exponential growth acceleration for body creation
- ✅ Splash screen with customization
- ✅ FPS-independent physics
- ✅ Detailed body information panel
- ✅ Vector visualization (velocity + force)

### Inspiration

This project was inspired by:
- Classical N-body simulations and orbital mechanics
- Space flight simulators (Kerbal Space Program, Universe Sandbox)
- Educational physics demonstrations
- The beauty and complexity of gravitational systems
- Khan Academy physics videos
- The three-body problem

### Special Thanks

To everyone who has:
- Reported bugs and suggested improvements
- Contributed code or documentation
- Shared their simulations and creations
- Provided encouragement and feedback

## 📸 Screenshots

*(Screenshots will be added soon to showcase features)*

**Planned screenshots:**
- Main simulation window with multiple bodies
- Vector visualization (velocity and force)
- Body information panel
- Chaotic multi-body system
- Binary orbit system
- Splash screen

## 🎓 Educational Use

Gravity Engine is perfect for:

- **Physics education** - Demonstrate Newton's laws and gravitational concepts
- **Programming learning** - Study game physics, Pygame, and Python
- **Scientific visualization** - Explore N-body problems and chaos theory
- **Mathematics** - Understand vectors, trigonometry, and calculus
- **Computational thinking** - Learn about optimization and algorithms
- **Entertainment** - Create beautiful orbital patterns and experiment

### Educational Topics Demonstrated

1. **Newton's Law of Universal Gravitation** - F = G(m₁m₂)/r²
2. **Momentum Conservation** - Total momentum before = after
3. **Center of Mass** - Position weighted by mass
4. **Kinetic Energy** - E = ½mv²
5. **Vector Addition** - Force and velocity decomposition
6. **Numerical Integration** - Euler method for physics
7. **Chaos Theory** - Sensitivity to initial conditions
8. **N-body Problem** - Classical unsolved problem in physics

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

**Gravity Reversal Experiment:**
1. Create several bodies
2. Press G to reverse gravity (bodies repel instead of attract)
3. Watch them fly apart!
4. Press G again to return to normal

**High-Speed Evolution:**
1. Generate random environment (P)
2. Increase time factor in config (`self.time_accelerationd = 1e4`)
3. Watch rapid evolution and mergers
4. Pause (Space) to examine the result

### Understanding the Display

**Main Info Panel (Top Left):**
- Number of bodies
- Total mass in system
- Heaviest body ID and mass
- Oldest body ID and age

**Selected Body Panel (Left Side):**
- Body ID
- Age (in simulated years)
- Mass (kg)
- Radius (m)
- Volume (m³)
- Density (kg/m³)
- Kinetic energy (J)
- Force applied (N)
- Velocity (m/s)
- Coordinates (x, y)
- Nearest body and distance

**Top Right:**
- Reversed gravity status
- Vectors display status
- Random mode status
- Random environment info

**Bottom:**
- Simulation age (years)
- Current FPS
- Time acceleration factor
- Pause status

### Tips for Best Results

- **Start small** - Begin with 2-5 bodies to understand the physics
- **Use pause** - Freeze time to set up specific scenarios
- **Experiment with settings** - Try different speeds, densities, etc.
- **Watch long-term** - Some systems take time to develop interesting behavior
- **Save screenshots** - Capture interesting moments (use OS screenshot tool)
- **Learn from failures** - Unstable systems teach as much as stable ones

---

## 🔧 Troubleshooting

### Common Issues

**Problem**: Font not found / Text doesn't display
- **Solution**: Ensure `assets/font.ttf` exists
- Check file path: `resource_path()` should find it automatically
- In PyInstaller builds, font must be in `assets/` folder

**Problem**: Music doesn't play
- **Solution**: Check `self.music = True` in config
- Ensure `assets/musics/` folder exists with MP3 files
- Music files must be named `music1.mp3`, `music2.mp3`, `music3.mp3`

**Problem**: Simulation runs too fast/slow
- **Solution**: Adjust `self.time_acceleration` in `Engine.__init__()`
- Lower values = slower simulation
- Higher values = faster simulation

**Problem**: Poor performance with many bodies
- **Solution**: See [Performance Tips](#performance-tips)
- Reduce body count
- Disable vectors (V key)
- Lower FPS target

**Problem**: Bodies disappear or behave strangely
- **Solution**: This can happen with extreme velocities
- Check for invalid coordinates (debug warnings in console)
- Reduce time acceleration (`self.time_acceleration`)
- Enable collision detection (`self.fusions = True`)

**Problem**: Can't create bodies
- **Solution**: Ensure you're clicking empty space (not on existing body)
- Try right-click or middle-click instead
- Check mouse is working properly

**Problem**: Executable won't run
- **Solution**: Rebuild using `make.bat` → Option [4]
- Check antivirus isn't blocking it
- Run from command line to see error messages

---

**⭐ Star this repository if you find it interesting!**

**Made with ❤️ and ☕ by [Nils DONTOT](https://github.com/Nitr0xis) (age 15)**

*Last updated: February 1, 2026*
*Version: 1.0.0 (as of code review)*

---

## 📚 Additional Resources

### Learning Resources

- **Newton's Laws** - [Khan Academy Physics](https://www.khanacademy.org/science/physics)
- **N-body Problem** - [Wikipedia](https://en.wikipedia.org/wiki/N-body_problem)
- **Pygame Documentation** - [pygame.org/docs](https://www.pygame.org/docs/)
- **Python Tutorial** - [python.org/tutorial](https://docs.python.org/3/tutorial/)

### Similar Projects

- **Universe Sandbox** - Commercial gravity simulator
- **Powder Game** - Browser-based physics sandbox
- **Algodoo** - 2D physics simulation educational software

### Further Reading

- "The Three-Body Problem" by Cixin Liu (science fiction)
- "Chaos: Making a New Science" by James Gleick
- "Numerical Recipes" by Press et al. (for optimization algorithms)

---

## 🎨 Color Scheme Reference

For developers modifying the code:

```python
# UI and General
WHITE = (255, 255, 255)      # Default body color (dark mode)
BLACK = (0, 0, 0)            # Background (dark mode)
BLUE = (10, 124, 235)        # UI text and info
DARK_GREY = (100, 100, 100)  # Body shadows/outlines

# Selection
DUCKY_GREEN = (28, 201, 89)  # Selection highlight

# Vectors
RED = (255, 0, 0)            # Global velocity vector
GREEN = (0, 255, 0)          # X-component velocity
YELLOW = (241, 247, 0)       # Y-component velocity
SP_BLUE = (130, 130, 220)    # Force vectors
```

---

## 🙏 Acknowledgments

- **Pygame** - Amazing game development library ([pygame.org](https://www.pygame.org/))
- **PyInstaller** - Executable building tool that makes distribution easy
- **Newton** - For the physics (obviously! 😄)
- **Python Community** - For excellent documentation and support
- **You** - For checking out this project and reading this far!

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
# 1. Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/GravityEngine.git
cd GravityEngine

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# Edit src/gravity_engine.py or other files

# 4. Test your changes
python src/gravity_engine.py

# 5. Commit with descriptive message
git add .
git commit -m "Add: detailed description of your changes"

# 6. Push and create pull request
git push origin feature/your-feature-name
```

### Code Style Guidelines

- **Follow PEP 8** - Python style guide (with reasonable flexibility)
- **Add docstrings** - Document classes and methods (see existing examples)
- **Comment physics** - Explain complex calculations and formulas
- **Keep functions focused** - Single responsibility principle
- **Test thoroughly** - Verify physics accuracy and edge cases
- **Use type hints** - Add type annotations where helpful

**Example documentation style (already used in code):**
```python
def fusion(self, other):
    """
    Merge two bodies, conserving momentum and mass.
    
    The larger body absorbs the smaller one. Position and velocity
    are calculated using center of mass and momentum conservation.
    
    Args:
        other: The other Circle object to merge with (will be destroyed)
    """
```

### Areas Needing Help

- 🐛 **Bug fixes** - Fix force averaging, unit inconsistencies
- ⚡ **Performance** - Implement QuadTree, spatial partitioning
- 📊 **Physics** - Add partial mass transfer, improve accuracy
- 🎨 **UI/UX** - Better selection indicators, info panels
- 📖 **Documentation** - Tutorials, examples, better comments
- 🌍 **Features** - Save/load, configuration files, presets

### Specific Contribution Ideas

1. **Fix force averaging bug** - Forces should be summed, not averaged
2. **Add QuadTree** - Optimize O(n²) to O(n log n)
3. **Create example scenarios** - Solar system, binary stars, etc.
4. **Add unit tests** - Test physics calculations
5. **Improve collision detection** - Broad-phase + narrow-phase
6. **Add save/load system** - JSON serialization
7. **Create documentation** - Physics formulas, usage guides

## 📝 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**.

[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Copyright © 2026 Nils DONTOT**

### You are free to:

- ✅ **Share** - Copy and redistribute the material in any medium or format
- ✅ **Adapt** - Remix, transform, and build upon the material

### Under the following terms:

- 📛 **Attribution** - Give appropriate credit to **Nils DONTOT**, provide a link to the license, and indicate if changes were made
- 🚫 **NonCommercial** - You may not use the material for commercial purposes
- 🔄 **ShareAlike** - If you remix, transform, or build upon the material, you must distribute your contributions under the same license

### What this means:

- ✅ Use for learning and education
- ✅ Modify for personal projects
- ✅ Share with attribution to Nils DONTOT
- ✅ Fork and improve (with same license)
- ❌ Sell or commercialize
- ❌ Use in paid products/services
- ❌ Remove attribution

See [LICENSE](LICENSE) for the complete legal text.

## 📧 Contact

**Nils DONTOT**

- 📧 **Email**: [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)
- 🐙 **GitHub**: [@Nitr0xis](https://github.com/Nitr0xis)
- 🔗 **Repository**: [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)
- 🌐 **Issues**: [Report bugs or suggest features](https://github.com/Nitr0xis/GravityEngine/issues)

### Get in Touch

- **Questions?** Open an issue or send an email
- **Ideas?** Share them in the issues section with the "enhancement" label
- **Collaboration?** Pull requests are welcome! Fork and submit
- **Bug reports?** Use the issue tracker with detailed reproduction steps


---

*Enjoy exploring the cosmos! 🌌*
