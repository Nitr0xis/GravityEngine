# GravityEngine

**v3.7.0** — N-body gravitational simulator built with Python and Pygame.

**Author:** Nils DONTOT  
**Repository:** [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)  
**Contact:** nils.dontot.pro@gmail.com

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)](https://www.pygame.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Nitr0xis-181717?logo=github)](https://github.com/Nitr0xis)

---

I am 15 years old and passionate about space and physics. In mid-2025, I decided to create a gravity simulator with Python. This is the result of my work. Feel free to submit pull requests if you identify potential improvements or optimization opportunities. I am constantly improving it, and I hope you like it.

---

## Table of Contents

- [Overview](#overview)
- [What's New in v3.7.0](#whats-new-in-v370)
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

## What's New in v3.7.0

### Gravitational Lensing Grid

A background grid rendered in world space, deformed per-vertex by the gravitational field of all active bodies. This is a visual approximation inspired by gravitational lensing — not a GR ray-tracing solution.

Technical properties:
- Each grid vertex is displaced using a Newtonian-inspired falloff: `falloff = soft² / (r² + soft²)`, which reaches ~1 near the body center and decays smoothly at distance, avoiding singularities.
- Deformation amplitude scales with `√(camera.scale)` so the effect remains perceptually stable across zoom levels, without distorting geometry at large or small scales.
- Softening is computed per body as `max(radius × 0.75, view_diagonal × 0.002, 8.0)` to prevent line crossings near dense bodies.
- Adaptive polyline sampling (~8 px per segment) keeps curves smooth without excessive vertex count.
- Minor grid (1/5 subdivisions) activates automatically when the major cell exceeds `grid_subdivide_px` in screen space.
- All parameters are configurable live via the config panel and persist to `saves/config.json`.
- Toggle: `B`. The `reversed_gravity` flag inverts deformation direction to match repulsion mode.

### Code Reorganization

`gravity_engine.py` (~3100 lines) has been fully decomposed into a flat module set. See [Architecture](#architecture) for the complete breakdown.

---

## Installation

**Prerequisites:** Python 3.11+, pip

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

Press `C` to open. Parameters take effect immediately; simulation continues in the background.

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

**Persistence:** `Save Config` / `Load Last Config` serialize all parameters to `saves/config.json`. The file stores the engine version alongside parameters; a version mismatch triggers a warning but still applies compatible keys.

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

The physics timestep is decoupled from render FPS. At each render frame, as many physics steps as needed are consumed from the time accumulator (up to 2 steps per frame to prevent spiral of death). Interpolation alpha `α = accumulator / timestep` bridges the gap for smooth rendering.

### Interpolated Rendering

All visual positions are interpolated between the previous and current physics states:

```
x_render = x_prev + (x - x_prev) × α
```

This applies to position, velocity, force, and radius. Click detection uses interpolated positions, so body selection targets what is visually on screen.

### Collision and Fusion

Detection uses overlap of visual (interpolated) radii, confirmed on physical radii. Fusion applies momentum conservation:

```
v_merged = (m₁v₁ + m₂v₂) / (m₁ + m₂)
m_merged = m₁ + m₂
r_merged = (3 × m_merged / (4π × density))^(1/3)
```

Kinetic energy is not conserved — the collision is perfectly inelastic by design.

### Adaptive Substeps

When enabled, each base physics step can be split into additional substeps based on relative body speeds and radii. This is a CCD-style mechanism to prevent fast-moving bodies from tunnelling through others. Controlled by `adaptive_substeps_max_extra` (0 = disabled, 8 = up to 9 substeps per base step).

---

## Architecture

Flat module structure under `src/`. No package hierarchy — all modules share state via `state.py`.

```
src/
├── engine.py               # Main loop, physics dispatch, render orchestration
├── state.py                # Shared globals: engine singleton + circles list
├── circle.py               # Body class: physics state, attraction, integration
├── camera.py               # World ↔ screen transforms, zoom, pan
├── action_manager.py       # Input event handlers (mouse, keyboard)
├── config_panel.py         # Overlay UI: sliders, checkboxes, buttons, scroll
├── gravitational_grid.py   # Background grid with gravitational lensing deformation
├── color.py                # Color class with arithmetic operators + Display palette
├── temp_text.py            # Timed on-screen notifications
├── utils.py                # Rendering helpers, aggregation (heaviest, oldest, mass_sum)
├── atlas.py                # Cross-platform asset and user-data path resolution
├── debugger.py             # Path diagnostics + physics unit tests
└── (tester.py)             # Extended test suite (determinism, interpolation cache)
```

### Shared State Pattern

`state.py` exposes two mutable globals:

```python
engine: Optional[Engine] = None
circles: list[Circle] = []
```

All modules import `state` and access `state.engine` / `state.circles` directly. This resolves circular imports (e.g. `Circle` needs engine settings, `Engine` holds `Circle` references) without rewriting to dependency injection. `circles` is always mutated in place — reassignment would silently break references held by other modules. Use `state.circles.clear()`, `append()`, `remove()`.

### Coordinate System

The camera maintains a linear transform: `screen = world × scale + offset`. `camera.screen_to_world` and `camera.world_to_screen` are the single source of truth. All physics runs in world space (meters); rendering converts to screen space at draw time.

### File Management

`Atlas` (`atlas.py`) handles dev/exe path differences transparently. In dev mode, user data goes to `user_data/` inside the project. In exe mode (PyInstaller), user data goes to `Documents/GravityEngine/`. Assets are always resolved via `fm.resource_path()`.

---

## Educational Use

GravityEngine demonstrates:

- Newton's law of universal gravitation (F = Gm₁m₂/r²)
- Momentum and mass conservation in inelastic collisions
- Fixed timestep integration and determinism
- Render/physics decoupling via linear interpolation
- World-to-screen coordinate transformation
- Zoom-adaptive scaling (body mass ∝ 1/scale²)
- Gravitational lensing approximation (visual, Newtonian-inspired)
- N-body problem (classical, O(n²) per step)
- Custom UI design in Pygame (overlay panels, animated widgets)
- Cross-platform file management (dev vs. exe detection)

---

## Troubleshooting

**Config panel not opening:** press `C`, not `Ctrl+C`. Check console for import errors.

**Font not found:** verify `assets/fonts/main_font.ttf` exists. Run `Debugger.default_debug()` to print path resolution.

**Help overlay not showing:** hold `H` or `I` — releasing dismisses it.

**Simulation too fast / slow:** open config (`C`), adjust Time Acceleration. Default is 2×10⁴.

**Gravitational grid invisible:** check `grid_lens_amount > 0` in config. At zoom-out extremes, deformation may be sub-pixel — zoom in or increase lens strength.

**Grid line crossings at high lens strength:** reduce `grid_lens_amount` (cap is 10). Crossings occur when displacement exceeds half the softening radius.

**Poor performance with grid enabled:** reduce `grid_max_lines` in source (default 64) or increase `grid_target_spacing_px` (fewer, wider lines).

**Screenshots not saving:** check `user_data/screenshots/` (dev) or `Documents/GravityEngine/screenshots/` (exe). Verify write permissions.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for complete history.

### Recently Completed

| Version | Feature |
|---|---|
| v3.7.0 | Gravitational lensing grid, code modularization |
| v3.6.0 | Code modularization |
| v3.5.0 | Configuration panel (Pygame overlay, custom widgets, save/load) |
| v3.3.0 | Interactive help overlay |
| v3.2.0 | Camera system rewrite, zoom-adaptive body generation |

### Current Focus (June 2026)

| Priority | Feature |
|---|---|
| 1 | Save / load simulation scenarios (JSON) |
| 2 | Predefined scenario presets |
| 3 | Performance profiling |
| 4 | CSV data export |

---

## Contributing

1. Fork and clone the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Test: `python src/engine.py`
4. Commit: `git commit -m "Add: feature description"`
5. Open a pull request

Priority areas: save/load system, scenario presets, performance profiling, data export.

---

## License

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**  
Copyright (c) 2026 Nils DONTOT

Non-commercial use and redistribution permitted with attribution. Derivative works must carry the same license.

See [LICENSE](LICENSE) — full terms at [creativecommons.org/licenses/by-nc-sa/4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

---

**Repository:** [github.com/Nitr0xis/GravityEngine](https://github.com/Nitr0xis/GravityEngine)  
**Issues:** [github.com/Nitr0xis/GravityEngine/issues](https://github.com/Nitr0xis/GravityEngine/issues)  
*Last updated: June 2026 — v3.7.0*
