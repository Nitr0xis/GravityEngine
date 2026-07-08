# Roadmap

## Current Focus

| Priority | Feature |
|---|---|
| 1 | Save / load simulation scenarios (JSON) |
| 2 | Predefined scenario presets |
| 3 | Performance profiling |
| 4 | CSV data export |

## Completed

- Rotating file logger for crash diagnostics
- Gravitational lensing grid (visual, Newtonian-inspired deformation)
- Full code modularization (flat module set under `src/`, shared `state.py`)
- Configuration panel (Pygame overlay, sliders/toggles, save/load to `saves/config.json`)
- Interactive help overlay
- Camera system rewrite (pan, zoom-at-mouse, reset)
- Zoom-adaptive body generation
- Fixed timestep physics with full interpolation (position, velocity, force, radius)
- Adaptive substeps (CCD-style, prevents tunnelling at high speed)

## Under Consideration

- QuadTree / Barnes-Hut for sub-O(n²) force calculation
- Trails and visual effects
- Multi-language support
- Background music system

Priorities can shift based on what's actually useful — this list isn't a contract. See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to pick up any of these.
