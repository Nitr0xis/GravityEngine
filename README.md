# GravityEngine

*N-body gravitational simulator built with Python and Pygame.*

**v3.8.0** — *Logging Edition*

**Author:** Nils DONTOT
**Repository:** [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)
**Contact:** nils.dontot.pro@gmail.com

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)](https://www.pygame.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Nitr0xis-181717?logo=github)](https://github.com/Nitr0xis)

---

I am 15 years old and passionate about space and physics. In mid-2025, I decided to create a gravity simulator with Python. This is the result of my work. Feel free to submit pull requests if you identify potential improvements or optimization opportunities. I am constantly improving it, and I hope you like it.

---

## Table of Contents

- [Overview](#overview)
- [What's New in v3.8](#whats-new-in-v38)
- [Installation](#installation)
- [Building Executables](#building-executables)
- [Controls](#controls)
- [Configuration Panel](#configuration-panel)
- [Physics](#physics)
- [Architecture](#architecture)
- [Educational Use](#educational-use)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

GravityEngine is an interactive N-body gravitational simulation. Create celestial bodies, watch them orbit, collide, and merge under Newtonian gravity, in real time.

<p align="center"><img src="previews/preview_1.png" width="80%" alt="Multiple bodies with velocity/force vectors"></p>

Key features:

- Pygame configuration panel with real-time parameter adjustment
- Gravitational lensing grid (visual, Newtonian-inspired)
- Fixed timestep physics (1/120s), deterministic simulation
- Full interpolation (position, velocity, force, radius) for smooth rendering
- Zoom-adaptive body generation, complete camera system (pan/zoom/reset)
- Cross-platform file manager (dev + exe)
- Rotating file logger for crash diagnostics
- Adaptive performance mode: 120 FPS with 100+ bodies

---

## What's New in v3.8 — Logging Edition

### File Logging

A rotating log system (`logger.py`) now records session events to `user_data/logs/gravityengine.log`. Purpose: diagnose crashes on `.exe` builds where the user has no console.

<p align="center"><img src="previews/preview_3.png" width="80%" alt="Gravitational lensing grid"></p>

The screenshot above shows the gravitational lensing grid (`B` to toggle), carried over from v3.7.

- Initialized once in `Engine.__init__` via `Logger.setup()`
- Standard levels: `info`, `warning`, `error`, `exception` (captures traceback automatically in `except` blocks)
- Log rotation: 1 MB per file, 3 backups kept
- No performance impact on the physics loop (file I/O only on discrete events, not per frame)

### Stability fixes (carried over from v3.7 refactor)

- Fixed `state` shadowing bug in `action_manager.py` and `circle.py` (local dict renamed to `istate`)
- Fixed duplicate `circles` list in `engine.py` causing invisible bodies

---

## Installation

**Prerequisites:** Python 3.13+, pip

```bash
pip install pygame matplotlib
```

**From source:**

```bash
git clone https://github.com/Nitr0xis/GravityEngine.git
cd GravityEngine
python src/engine.py
```

**Pre-built binary (Windows):** download `GravityEngine.exe` from [Releases](https://github.com/Nitr0xis/GravityEngine/releases). No Python required.

**Virtual environment (recommended):**

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
pip install pygame matplotlib
python src/engine.py
```

---

## Building Executables

Scripts are in `builders/`:

```bash
builders/build_release.bat   # Production binary
builders/build.bat           # Development binary
builders/clean.bat           # Clean dist/build artifacts
```

Manual PyInstaller command:

```bash
pyinstaller --onefile --windowed --add-data "assets;assets" --name GravityEngine src/engine.py
```

Assets are bundled via `--add-data "assets;assets"`. Path resolution uses `sys._MEIPASS` detection at runtime.

---

## Controls

### Camera

| Input | Action |
|---|---|
| Right click + drag | Pan |
| Mouse wheel | Zoom in / out (cursor-centered) |
| `A` / `E` | Zoom in / out (screen-centered) |
| Arrow keys | Pan |
| `T` | Reset camera |

### Bodies

| Input | Action |
|---|---|
| Left click (empty space) | Create body |
| Left click + hold | Grow body exponentially |
| Left click (on body) | Select body |
| `Del` | Delete selected body |

<p align="center"><img src="previews/preview_2.png" width="80%" alt="Selected body orbiting a star"></p>

### Simulation

| Key | Action |
|---|---|
| `Space` | Pause / resume |
| `V` | Toggle velocity / force vectors |
| `B` | Toggle gravitational lensing grid |
| `G` | Toggle reversed gravity (repulsion) |
| `R` | Toggle random velocity mode |
| `P` | Generate 20 random bodies (zoom-adaptive) |
| `S` | Save screenshot |
| `C` | Open / close configuration panel |
| `H` / `I` (hold) | Display help overlay |
| `Escape` | Exit (or close config panel if open) |

---

## Configuration Panel

Press `C` to open. Parameters take effect immediately.

<p align="center"><img src="previews/preview_4.png" width="80%" alt="Configuration panel"></p>

**Simulation**

| Parameter | Range | Default |
|---|---|---|
| Target FPS | 30–240 | 120 |
| Time Acceleration | 10³–10⁵× | 2×10⁴ |

**Physics**

| Parameter | Type | Default |
|---|---|---|
| Reversed Gravity | toggle | off |
| Random Speed Mode | toggle | off |
| Body Density | 1–10⁵ kg/m³ (log) | 5514 kg/m³ |
| Enable Fusions | toggle | on |

**Visual**

| Parameter | Type | Default |
|---|---|---|
| Camera Zoom | 10⁻⁷–100× (log) | 1× |
| Show Vectors | toggle | off |
| Vector Scale | 0.1–10× | 1× |
| Gravitational Grid | toggle | off |
| Grid Lens Strength | 0–10 | 3.5 |
| Grid Spacing | 40–160 px | 72 px |

**Advanced (Collisions)**

| Parameter | Type | Default |
|---|---|---|
| Adaptive Substeps | toggle | off |
| Substep Precision | +0–8 steps | 0 |

**Persistence:** `Save Config` / `Load Last Config` serialize all parameters to `saves/config.json`. Version mismatch triggers a warning but still applies compatible keys.

---

## Physics

### Gravitational Force

```
F = G × m₁ × m₂ / r²      G = 6.6743 × 10⁻¹¹ N·m²/kg²
```

### Integration

Fixed timestep (1/120 s), explicit Euler:

```
x(t+dt) = x(t) + v(t) × dt
v(t+dt) = v(t) + (F/m) × dt
```

Physics timestep is decoupled from render FPS. Each render frame consumes as many physics steps as needed from the accumulator (capped at 2 to avoid spiral of death). Interpolation alpha `α = accumulator / timestep` bridges the gap for rendering.

### Interpolated Rendering

```
x_render = x_prev + (x - x_prev) × α
```

Applies to position, velocity, force, radius. Click detection uses interpolated positions, so selection targets what is visually on screen.

### Collision and Fusion

Detection uses overlap of visual (interpolated) radii, confirmed on physical radii. Momentum conservation only:

```
v_merged = (m₁v₁ + m₂v₂) / (m₁ + m₂)
m_merged = m₁ + m₂
r_merged = (3 × m_merged / (4π × density))^(1/3)
```

Kinetic energy is not conserved — perfectly inelastic collision by design.

### Adaptive Substeps

Each base physics step can split into extra substeps based on relative speed and radii (CCD-style, prevents tunnelling). Controlled by `adaptive_substeps_max_extra` (0 = disabled, 8 = up to 9 substeps).

---

## Architecture

Flat module structure under `src/`. All modules share state via `state.py`.

```
src/
├── main.py               # Main loop, physics dispatch, render orchestration
├── state.py                # Shared globals: engine singleton + circles list
├── circle.py                # Body class: physics state, attraction, integration
├── camera.py                # World ↔ screen transforms, zoom, pan
├── action_manager.py        # Input event handlers (mouse, keyboard)
├── config_panel.py          # Overlay UI: sliders, checkboxes, buttons, scroll
├── gravitational_grid.py    # Background grid with lensing deformation
├── color.py                 # Color class with arithmetic operators + palette
├── temp_text.py              # Timed on-screen notifications
├── utils.py                  # Rendering helpers, aggregation (heaviest, oldest, mass_sum)
├── atlas.py                  # Cross-platform asset and user-data path resolution
├── logger.py                 # Rotating file logger (new in v3.8)
└── debugger.py                # Path diagnostics + physics unit tests
```

### Shared State Pattern

```python
engine: Optional[Engine] = None
circles: list[Circle] = []
```

All modules import `state` and access `state.engine` / `state.circles` directly. Resolves circular imports (`Circle` needs engine settings, `Engine` holds `Circle` references) without dependency injection. `circles` is always mutated in place — reassignment breaks references held elsewhere. Use `state.circles.clear()`, `append()`, `remove()`.

### Coordinate System

`camera.screen_to_world` / `camera.world_to_screen` are the single source of truth for `screen = world × scale + offset`. Physics runs in world space (meters); rendering converts to screen space at draw time.

### File Management

`Atlas` (`atlas.py`) handles dev/exe path differences transparently. Dev mode: user data in `user_data/` inside the project. Exe mode (PyInstaller): user data in `Documents/GravityEngine/`. Assets always resolved via `fm.resource_path()`.

### Logging

`Logger` (`logger.py`) is a static wrapper around `logging.Logger`, initialized once via `Logger.setup(engine.logs_folder_path)`. Rotating file handler, 1 MB per file, 3 backups. Use `Logger.exception()` inside `except` blocks to capture the traceback automatically.

---

## Educational Use

GravityEngine demonstrates:

- Newton's law of universal gravitation (F = Gm₁m₂/r²)
- Momentum and mass conservation in inelastic collisions
- Fixed timestep integration and determinism
- Render/physics decoupling via linear interpolation
- World-to-screen coordinate transformation
- Gravitational lensing approximation (visual, Newtonian-inspired)
- N-body problem (classical, O(n²) per step)
- Custom UI design in Pygame

---

## Troubleshooting

**Config panel not opening:** press `C`, not `Ctrl+C`. Check console/log for import errors.

**Font not found:** verify `assets/fonts/main_font.ttf` exists. Run `Debugger.default_debug()` to print path resolution.

**Simulation too fast / slow:** open config (`C`), adjust Time Acceleration (default 2×10⁴).

**Gravitational grid invisible:** check `grid_lens_amount > 0`. At extreme zoom-out, deformation may be sub-pixel — zoom in or increase lens strength.

**Grid line crossings at high lens strength:** reduce `grid_lens_amount` (cap 10).

**Poor performance with grid enabled:** reduce `grid_max_lines` (default 64) or increase `grid_target_spacing_px`.

**Screenshots not saving:** check `user_data/screenshots/` (dev) or `Documents/GravityEngine/screenshots/` (exe). Verify write permissions.

**Crash with no visible error (exe build):** check `user_data/logs/gravityengine.log` (or `Documents/GravityEngine/logs/` in exe mode) for the traceback.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for complete history.

### Recently Completed

| Version | Feature |
|---|---|
| v3.8.0 | Rotating file logger |
| v3.7.0 | Gravitational lensing grid, code modularization |
| v3.5.0 | Configuration panel (Pygame overlay, save/load) |
| v3.3.0 | Interactive help overlay |
| v3.2.0 | Camera system rewrite, zoom-adaptive body generation |

### Current Focus

| Priority | Feature |
|---|---|
| 1 | Save / load simulation scenarios (JSON) |
| 2 | Predefined scenario presets |
| 3 | Performance profiling |
| 4 | CSV data export |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Quick version:

1. Fork and clone the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Test: `python src/engine.py`
4. Commit: `git commit -m "feat: description"`
5. Open a pull request

Priority areas: save/load system, scenario presets, performance profiling, data export.

---

## License

**MIT License**
Copyright (c) 2026 Nils DONTOT

Permissive license: use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software freely, including in commercial contexts, provided the copyright notice and license text are retained.

See [LICENSE](LICENSE) — full terms at [opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

---

**Repository:** [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)
**Issues:** [github.com/Nitr0xis/GravityEngine/issues](https://github.com/Nitr0xis/GravityEngine/issues)

Made with ❤ by Nils DONTOT.

*Last updated: July 2026 — v3.8.0*
