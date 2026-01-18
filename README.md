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

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Controls](#controls)
- [Configuration](#configuration)
- [Physics](#physics)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🌌 Overview

Gravity Engine is an interactive physics simulation that allows you to create and observe celestial bodies interacting under Newtonian gravity. Watch bodies orbit, collide, and merge in real-time with adjustable parameters and visualization options.

**Developed by Nils DONTOT** - [GitHub Profile](https://github.com/NilsDontot)

![Gravity Engine Demo](assets/demo.gif) *(Add a demo GIF here)*

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
   python src/main.py
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
python src/main.py
```

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

You can modify simulation parameters in the `Engine.__init__()` method:
```python
# Display settings
self.FULLSCREEN = True          # Fullscreen mode
self.screen_mode = "dark"       # "dark" or "light"
self.FPS = 120                  # Target frame rate

# Physics settings
self.speed = 1_000_000_00       # Time acceleration factor
self.gravity = 6.6743e-11       # Gravitational constant (G)
self.fusions = True             # Enable/disable body fusion

# Visualization
self.vectors_printed = False    # Show velocity vectors
self.strength_vectors = True    # Show force vectors
self.cardinal_vectors = False   # Show X/Y velocity components

# Random generation
self.random_mode = False        # Random initial velocities
self.random_field = 1e-17       # Random velocity energy (kJ)
self.random_environment_number = 20  # Bodies in random environment
```

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

*(Add screenshots here showing different features)*

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
