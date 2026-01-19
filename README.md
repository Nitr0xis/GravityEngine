# Gravity Engine

A real-time N-body gravitational simulation built with Python and Pygame.

**Created by [Nils DONTOT](https://github.com/NilsDontot)**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)](https://www.pygame.org/)
[![GitHub](https://img.shields.io/badge/GitHub-NilsDontot-181717?logo=github)](https://github.com/NilsDontot)

---

**Author:** Nils DONTOT  
**Repository:** [github.com/NilsDontot/GravityEngine](https://github.com/NilsDontot/GravityEngine)  
**Email:** [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)

---

## 📋 Table of Contents

- [Before We Begin](#-before-we-begin)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#-project-structure)
- [Controls](#controls)
- [Configuration](#configuration)
- [Physics](#physics)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🪶 Before We Begin

Hello, I am 15 years old and I am passionate about programming and physics. That is why I decided in mid-2025 to create a gravity simulator with Python. Here is the result of my work. I am constantly trying to improve it, and I hope you like it.

Every previous changes are avaiable in [ROADMAP.md](ROADMAP.md).

## 🌌 Overview

Gravity Engine is an interactive physics simulation that allows you to create and observe celestial bodies interacting under Newtonian gravity. Watch bodies orbit, collide, and merge in real-time with adjustable parameters and visualization options.

**Developed by Nils DONTOT** - [GitHub Profile](https://github.com/NilsDontot)

![Gravity Engine Demo](assets/demo.gif) *(A demo gif will soon be added)*

## ✨ Features

### Current Features
- ✅ Real-time N-body gravitational simulation
- ✅ Interactive body creation with mouse controls
- ✅ Body fusion on collision with momentum conservation
- ✅ Velocity and force vector visualization
- ✅ Detailed body information display (mass, velocity, energy, etc.)
- ✅ Pause/resume functionality
- ✅ Random initial velocity mode
- ✅ Reversed gravity mode
- ✅ FPS correction system for consistent simulation speed
- ✅ Fullscreen support with native resolution detection
- ✅ Random environment generation

### Planned Features
See [ROADMAP.md](ROADMAP.md) for upcoming features and development timeline.

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
```bash
   git clone https://github.com/NilsDontot/GravityEngine.git
   cd GravityEngine
```

2. **Install dependencies**
   
   The program will automatically install required dependencies on first run, or you can install them manually:
```bash
   pip install pygame
```

3. **Run the simulation**
```bash
   python src/gravity_engine.py
```

### Manual Installation

If you prefer to install dependencies manually:
```bash
# Create virtual environment (optional but recommended)
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
├── src/
│   └── gravity_engine.py                 # Main program file - run this to start
│
├── assets/
│   ├── icon.ico                # executable icon
│   ├── font.ttf                # UI font (required)
│   ├── music1.mp3              # Unavaiable (feature in development)
│   ├── music2.mp3              # Unavaiable (feature in development)
│   └── music3.mp3              # Unavaiable (feature in development)
│
├── README.md                   # This file
├── ROADMAP.md                  # Development roadmap and timeline
├── LICENSE                     # License information (CC BY-NC-SA 4.0)
├── .gitignore                  # Git ignore rules
└── .gitattributes              # Git attributes configuration
```

### Important Files

| File | Description | Required |
|------|-------------|----------|
| `app/gravity_engine.exe` | Main simulation executable | 📖 Recommended (actually doesn't work) |
| `src/gravity_engine.py` | Main simulation program | ✅ Required |
| `assets/font.ttf` | UI font file | ✅ Required |
| `assets/music*.mp3` | Background music files | 🚫 Feature under development |
| `README.md` | Documentation | 📖 Recommended |
| `ROADMAP.md` | Development timeline | 📖 Recommended |
| `LICENSE` | License terms | ⚖️ Legal |

### File Locations

- **Main executable**: `src/gravity_engine.exe`
- **Main source code**: `src/gravity_engine.py`
- **Configuration**: Edit parameters in `Engine.__init__()` within `src/gravity_engine.py`
- **Font**: Place your `.ttf` font file in `assets/font.ttf`
- **Music**: Place `.mp3` files in `assets/` (if using background music) [ ⚠️ feature in development]

> 💡 **Tip**: If the `assets/` folder doesn't exist, create it manually and add your font file before running the program.

## 🎮 Controls

### Mouse Controls
- **Left Click** - Create a new body (hold to increase size)
- **Right Click** - Create a new body (hold to increase size)
- **Mouse Wheel** - Create smallest possible bodies
- **Click on Body** - Select/deselect a body

### Keyboard Controls
| Key | Action |
|-----|--------|
| `Space` | Pause/unpause simulation |
| `V` | Toggle velocity vectors display |
| `R` | Toggle random velocity mode |
| `G` | Toggle reversed gravity |
| `P` | Generate random environment (20 bodies) |
| `Delete` | Delete selected body |
| `Escape` | Exit program |

## ⚙️ Configuration

You can modify simulation parameters in the `Engine.__init__()` method. Parameters are organized into logical sections:

### Display Settings
```python
self.FULLSCREEN = True              # Enable fullscreen mode
self.screen_mode = "dark"           # Color scheme: "dark" or "light"
```

### UI Settings
```python
self.txt_size = 30                  # Font size for UI text
self.txt_gap = 15                   # Spacing between text lines
self.info_y = 20                    # Y position for info display
```

### Physics Settings
```python
self.G = 6.6743e-11                 # Gravitational constant (m³ kg⁻¹ s⁻²)
self.gravity = self.G               # Active gravitational constant
self.fusions = True                 # Enable/disable body fusion on collision
```

### Simulation Settings
```python
self.FPS = 120                      # Target frames per second
self.speed = 1_000_000_00           # Time acceleration factor
self.growing_speed = 0.5            # Body growth rate when creating
```

### Visualization Settings
```python
self.vectors_printed = False        # Show velocity vectors by default
self.strength_vectors = True        # Show force vectors
self.cardinal_vectors = False       # Show X/Y velocity components
self.vectors_in_front = True        # Draw vectors on top of bodies
self.vector_length = 1              # Vector display scale multiplier
```

### Random Generation Settings
```python
self.random_mode = False            # Random initial velocities on creation
self.random_field = 1e-17           # Random velocity energy in kJ
self.random_environment_number = 20 # Bodies created with 'P' key
```

### Audio Settings
```python
self.music = False                  # Enable/disable background music
self.music_volume = 1               # Music volume (0.0 to 1.0)
```

### Quick Configuration Examples

#### Create a Slower, More Visible Simulation
```python
self.speed = 1_000_000              # Reduce time acceleration
self.vectors_printed = True         # Show vectors by default
self.vector_length = 2              # Make vectors longer
```

#### High-Performance Mode
```python
self.FPS = 60                       # Lower FPS for better performance
self.vectors_printed = False        # Disable vectors
self.strength_vectors = False       # Disable force vectors
```

#### Chaotic System
```python
self.random_mode = True             # Random initial velocities
self.random_field = 1e-16           # Higher random energy
self.reversed_gravity = True        # Reverse gravity direction
```

#### Solar System-like Setup
```python
self.speed = 10_000_000             # Moderate time acceleration
self.fusions = False                # Prevent planets from merging
self.random_mode = False            # Controlled initial conditions
```

### Advanced Configuration

For more advanced modifications, you can edit:

- **Body creation parameters** in `Circle.__init__()`
- **Force calculations** in `Circle.attract()`
- **Collision behavior** in `Circle.fusion()`
- **Keyboard mappings** in `Engine.run()` → `KEY_MAP`

### Configuration File (Future Feature)

> 📋 **Coming Soon**: External configuration file support (JSON/YAML) is planned for Q2 2026. See [ROADMAP.md](ROADMAP.md) for details.

## 🔬 Physics

### Gravitational Force

The simulation uses Newton's law of universal gravitation:
```
F = G × (m₁ × m₂) / r²
```

Where:
- `F` = gravitational force (N)
- `G` = gravitational constant (6.6743 × 10⁻¹¹ m³ kg⁻¹ s⁻²)
- `m₁, m₂` = masses of the two bodies (kg)
- `r` = distance between bodies (m)

### Body Fusion

When two bodies collide (distance < sum of radii), they merge conserving:
- **Mass**: `m_new = m₁ + m₂`
- **Momentum**: `p_new = p₁ + p₂`
- **Position**: Weighted by mass
- **Velocity**: Calculated from momentum conservation

The new radius is calculated as: `r_new = ∛(m_new)`

### Units

| Property | Unit | Symbol |
|----------|------|--------|
| Mass | Tonnes | t |
| Distance | Meters | m |
| Time | Seconds | s |
| Force | Newtons | N |
| Energy | Joules | J |
| Velocity | Meters/second | m/s |

> ⚠️ **Note**: The current unit system is being revised. See [ROADMAP.md](ROADMAP.md) for planned improvements.

## 📊 Performance

Current performance characteristics:
- **O(n²) complexity** for gravitational calculations
- Suitable for up to ~100 bodies at 60 FPS
- FPS-independent physics simulation

Planned optimizations (see [ROADMAP.md](ROADMAP.md)):
- QuadTree or Barnes-Hut algorithm implementation
- GPU acceleration with CUDA
- Multi-threading support

## 📈 Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plans and timelines.
Previous features and deadlines are described into the file.

### Q1 2026 Priorities
1. ✅ Coherent physical units
2. ✅ Relative display system (screen-independent)
3. ⏳ Partial mass transfer on collision
4. ⏳ Optimized position calculation (QuadTree/Barnes-Hut)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue describing the bug
2. **Suggest features** - Open an issue with your feature request
3. **Submit pull requests** - Fork, create a branch, and submit a PR

### Development Setup
```bash
# Fork and clone your fork
git clone https://github.com/NilsDontot/GravityEngine.git
cd GravityEngine

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "Add your feature"

# Push and create a pull request
git push origin feature/your-feature-name
```

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to classes and methods
- Comment complex physics calculations
- Keep functions focused and concise

## 📝 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**.

[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Copyright © 2026 Nils DONTOT**

This means you are free to:
- ✅ **Share** - copy and redistribute the material
- ✅ **Adapt** - remix, transform, and build upon the material

Under the following terms:
- 📛 **Attribution** - Give appropriate credit to **Nils DONTOT**
- 🚫 **NonCommercial** - Not for commercial purposes
- 🔄 **ShareAlike** - Distribute under the same license

See [LICENSE](LICENSE) for the full license text.

## 📧 Contact

**Nils DONTOT**

- 📧 Email: [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)
- 🐙 GitHub: [@NilsDontot](https://github.com/NilsDontot)
- 🔗 Repository: [github.com/NilsDontot/GravityEngine](https://github.com/NilsDontot/GravityEngine)

## 🙏 Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classical N-body simulations
- Developed by [Nils DONTOT](https://github.com/NilsDontot)

## 📸 Screenshots

*(Screenshots showing different features will soon be added)*

### Main Simulation
![Main View](assets/screenshot1.png)

### Vector Visualization
![Vectors](assets/screenshot2.png)

### Body Information
![Info Panel](assets/screenshot3.png)

---

**⭐ Star this repository if you find it interesting!**

**Made with ❤️ by [Nils DONTOT](https://github.com/NilsDontot)**

*Last updated: January 18, 2026*
