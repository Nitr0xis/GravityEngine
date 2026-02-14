# Gravity Engine

A real-time N-body gravitational simulation built with Python and Pygame.

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
- [Performance](#-performance)
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

The simulation features accurate Newtonian physics with momentum conservation, fixed timestep integration for determinism, smooth rendering with interpolation, and multiple visualization modes. Whether you want to recreate a solar system, observe chaotic three-body problems, or simply experiment with gravitational interactions, Gravity Engine provides an intuitive interface for exploration.

**Key Technical Features:**
- **Fixed timestep physics** - Deterministic simulation regardless of rendering FPS
- **Interpolated rendering** - Smooth 120 FPS visuals even with variable frame rates
- **Time accumulator system** - Precise physics updates with "spiral of death" prevention
- **Momentum conservation** - Physically accurate collisions and mergers

**Developed by Nils DONTOT** - [GitHub Profile](https://github.com/Nitr0xis)

![Gravity Engine Demo](assets/demo.gif) *(A demo gif will soon be added)*

## ✨ Features

### Current Features (February 2026)
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

### Recent Improvements (February 2026)
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
self.splash_screen_font = resource_path('assets/fonts/toruk.ttf')
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

### Timestep Settings (NEW)
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
self.time_acceleration = 1e7            # Time acceleration factor
self.growing_speed = 0.1                # Base body growth rate when creating
```

### UI Settings
```python
self.used_font = resource_path('assets/fonts/main_font.ttf')
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
self.minimum_mass = 1000                # Minimum mass for new bodies (kg)
self.default_density = 5515             # Default density (kg/m³) - Earth density
```

### Visualization Settings
```python
self.vectors_printed = False            # Show velocity vectors by default
self.force_vectors = True               # Show force vectors
self.cardinal_vectors = False           # Show X/Y velocity components separately
self.vectors_in_front = True            # Draw vectors on top of bodies
self.vector_scale = 1                   # Vector display scale multiplier
```

### Random Generation Settings
```python
self.random_mode = False                # Random initial velocities on creation
self.random_environment_number = 20     # Bodies created with 'P' key

# Maximum kinetic energy for random velocities
max_kinetic_energy_joules = 5e-5        # in Joules
self.random_field = max_kinetic_energy_joules / (self.FPS_TARGET ** 2)
```

### Audio Settings
```python
self.musics_folder_path = resource_path('assets/musics')
self.music = False                      # Enable/disable background music
self.music_volume = 1                   # Music volume (0.0 to 1.0)
```

### Quick Configuration Examples

#### High-Performance Mode
```python
self.FPS_TARGET = 60                    # Lower FPS for better performance
self.vectors_printed = False            # Disable vectors
self.force_vectors = False              # Disable force vectors
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
```

## 🔬 Physics

### Fixed Timestep Integration (NEW)

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

### Interpolated Rendering (NEW)

Rendering uses **linear interpolation** (alpha blending) between physics states:

```python
# Alpha = progress between current and next physics step
alpha = time_accumulator / physics_timestep  # 0.0 to 1.0

# Interpolated position
render_x = prev_x + (x - prev_x) * alpha
render_y = prev_y + (y - prev_y) * alpha
```

**Result:** Smooth 120 FPS display even when physics runs at fixed intervals.

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

### Force Vector Visualization (IMPROVED)

Force vectors now use **logarithmic scaling** with **direction preservation**:

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
| Density | kg/m³ | - | Default: 5515 (Earth) |

### Testing Framework (NEW)

The `Tester` class includes unit tests:

```python
Tester.test_force_summation()    # Verify forces are summed correctly
Tester.test_determinism()        # Verify same inputs → same outputs
Tester.test_uniform_speed()      # Verify FPS-independent physics
```

## 📊 Performance

### Current Performance

- **Algorithm**: O(n²) brute-force gravitational calculations
- **Optimal range**: Up to ~50-100 bodies at 120 FPS (depends on hardware)
- **Physics**: Fixed timestep ensures consistent accuracy
- **Rendering**: Interpolated for smooth 120 FPS
- **Memory**: ~50-100 MB typical usage

### Performance Characteristics

**Fixed timestep benefits:**
- ✅ Consistent physics regardless of rendering FPS
- ✅ Deterministic simulation (same inputs → same outputs)
- ✅ No "time dilation" from slow frames
- ✅ Predictable behavior

**Performance factors:**
- **Body count** - Quadratic scaling (O(n²))
- **Vector rendering** - Each vector drawn separately (with interpolation)
- **Force calculations** - All pairs calculated every physics step
- **Interpolation** - Minimal overhead for smooth rendering

### Performance Tips

1. **Reduce body count** - Fewer bodies = dramatically faster (O(n²) complexity)
2. **Disable vectors** - Turn off visualization (V key)
3. **Lower FPS target** - `self.FPS_TARGET = 60` instead of 120
4. **Disable force vectors** - `self.force_vectors = False`
5. **Adjust time acceleration** - Higher values = faster evolution

### Benchmarks (Approximate)

| Bodies | FPS (120 target) | Physics Steps/Frame |
|--------|------------------|---------------------|
| 10 | 120 | 1 |
| 50 | 100-120 | 1 |
| 100 | 60-80 | 1-2 |
| 200 | 30-40 | 2-3 |
| 500+ | <20 | 5+ |

> 💡 With fixed timestep, slow frames just mean more physics steps per render.

## 📈 Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plans and timelines.

### Recently Completed (February 2026)

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

- **February 2026**: Scale factor implementation, unit system finalization
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
- Default: `1e7` (10 million × real time)
- Lower = slower simulation, Higher = faster simulation

**Problem**: Poor performance with many bodies
- **Solution**: 
  - Reduce body count
  - Disable vectors (V key)
  - Lower FPS target: `self.FPS_TARGET = 60`
  - Disable force vectors: `self.force_vectors = False`

**Problem**: Bodies behave strangely or disappear
- **Solution**: 
  - Check for extreme velocities
  - Reduce time acceleration
  - Enable collision detection (`self.fusions = True`)

**Problem**: Vectors don't align with bodies
- **Solution**: This was fixed in February 2026 with interpolated rendering
- Update to latest version if using older code

**Problem**: Physics changes with different FPS
- **Solution**: This was fixed with fixed timestep integration
- Physics now runs at consistent 1/120s regardless of rendering FPS

## 🎓 Educational Use

Gravity Engine is perfect for:

- **Physics education** - Demonstrate Newton's laws and gravitational concepts
- **Programming learning** - Study game physics, Pygame, and Python
- **Scientific visualization** - Explore N-body problems and chaos theory
- **Mathematics** - Understand vectors, trigonometry, and numerical integration
- **Computational thinking** - Learn about optimization and algorithms

### Educational Topics Demonstrated

1. **Newton's Law of Universal Gravitation** - F = G(m₁m₂)/r²
2. **Momentum Conservation** - Total momentum before = after
3. **Fixed Timestep Integration** - Deterministic physics simulation
4. **Interpolation** - Smooth rendering between discrete states
5. **Numerical Stability** - Time accumulator and spiral-of-death prevention
6. **Kinetic Energy** - E = ½mv²
7. **Vector Mathematics** - Force and velocity decomposition
8. **N-body Problem** - Classical unsolved problem in physics

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

*Last updated: February 14, 2026*  
*Version: 2.0.0 - Fixed Timestep Edition*

---

*Enjoy exploring the cosmos! 🌌*
