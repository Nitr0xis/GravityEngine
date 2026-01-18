# Roadmap - Gravity Engine

## Overview
This document outlines the development roadmap for Gravity Engine with prioritized objectives and their deadlines.

---

## Q1 2026 (January - March)

### ✅ January 2026 (Completed)
- [x] Fixed collision detection for recently created circles
- [x] Implemented temporary text system (TempText)
- [x] Improved fullscreen display mode management
- [x] Collision detection by distance rather than rect

### 🔄 February 2026 (In Progress)
**Deadline: February 28, 2026**

#### Priority 1: Coherent Physical Units
- [ ] Complete revision of unit system
  - [ ] Add corpses density
  - [ ] Standardize masses (currently in tonnes)
  - [ ] Standardize distances (currently in meters/pixels)
  - [ ] Verify and correct gravitational constant G
  - [ ] Fix force and kinetic energy formulas
- [ ] Documentation of units used in code
- [ ] Physical calculation validation tests

#### Priority 2: Relative Display System
- [ ] Replace absolute pixel display
  - [ ] Create normalized coordinate system (0.0 - 1.0)
  - [ ] Implement scale coefficient based on resolution
  - [ ] Adapt all UI elements (text, positions, sizes)
- [ ] Enhanced multi-resolution support
  - [ ] Test on different resolutions (1080p, 1440p, 4K)
  - [ ] Dynamically adapt font sizes
  - [ ] Handle variable aspect ratios

### 📅 March 2026
**Deadline: March 31, 2026**

#### Priority 1: Partial Mass Transfer
- [ ] Implement elastic/inelastic collision logic
  - [ ] Detect non-fusion collisions
  - [ ] Calculate mass transfer based on relative velocity
  - [ ] Calculate kinetic energy transfer
  - [ ] Implement momentum conservation
- [ ] Configurable collision parameters
  - [ ] Fusion vs simple collision threshold
  - [ ] Coefficient of restitution
  - [ ] Transferable mass percentage
- [ ] Visual effects for partial collisions
  - [ ] Collision animation
  - [ ] Temporary transfer notification

#### Priority 2: Optimized Position Calculation System
- [ ] Research and design
  - [ ] Study QuadTree implementation
  - [ ] Analyze Barnes-Hut algorithm
  - [ ] Compare expected performance
- [ ] Implementation of chosen system
  - [ ] Optimized data structure
  - [ ] Spatial search algorithm
  - [ ] Optimized force calculations (avoid O(n²))
- [ ] Performance testing
  - [ ] Benchmarks with 10, 50, 100, 500 bodies
  - [ ] Before/after optimization comparison
  - [ ] Parameter tuning

#### Priority 3: Finish music features development
- [ ] Setup assets/music*.mp3

---

## Q2 2026 (April - June)

### April 2026
**Deadline: April 30, 2026**

- [ ] Advanced camera system
  - [ ] Functional mouse wheel zoom
  - [ ] Smooth panning
  - [ ] Auto-follow selected body
  - [ ] Navigation mini-map

- [ ] Enhanced user interface
  - [ ] In-game settings menu
  - [ ] Simulation configuration panel
  - [ ] Configurable keyboard shortcuts

### May 2026
**Deadline: May 31, 2026**

- [ ] Save/Load system
  - [ ] Export simulation to JSON
  - [ ] Import simulation
  - [ ] Auto-save functionality
  - [ ] Scenario preset management

- [ ] Predefined simulation modes
  - [ ] Solar system
  - [ ] Binary system
  - [ ] Stellar cluster
  - [ ] Galaxy collision

### June 2026
**Deadline: June 30, 2026**

- [ ] Performance improvements
  - [ ] Code profiling
  - [ ] Critical loop optimization
  - [ ] NumPy for vectorized calculations
  - [ ] Multi-threading support if possible

---

## Q3 2026 (July - September)

### July - September 2026

- [ ] Advanced visual effects
  - [ ] Motion trails
  - [ ] Enhanced collision effects
  - [ ] Reference grid
  - [ ] Predicted trajectory display

- [ ] Analysis tools
  - [ ] Total energy graphs
  - [ ] Momentum graphs
  - [ ] Real-time statistics
  - [ ] Data export for analysis

- [ ] Complete documentation
  - [ ] User guide
  - [ ] API documentation
  - [ ] Video tutorials

---

## Backlog (No Fixed Date)

### Future Features
- [ ] GPU calculations with CUDA/OpenCL
  - Support thousands of bodies simultaneously
  - Massive calculation acceleration

- [ ] 3D Mode
  - Three-dimensional simulation
  - Rotating 3D camera
  - OpenGL/Vulkan rendering

- [ ] Advanced physics
  - Body deformation
  - Fragmentation on violent collisions
  - Hawking radiation (black holes)
  - Simplified general relativity

- [ ] Network/Multiplayer
  - Collaborative simulations
  - Online scenario sharing
  - Leaderboards

- [ ] AI/ML
  - Trajectory prediction
  - Automatic parameter optimization
  - Procedural generation of stable systems

### Technical Improvements
- [ ] Comprehensive unit tests
- [ ] CI/CD pipeline
- [ ] Packaging (PyPI, standalone executable)
- [ ] Native macOS/Linux support

---

## Development Notes

### Current Technical Constraints
- Performance limited to ~100 bodies with O(n²) calculation
- 2D display only
- CPU calculations only
- No advanced collision handling

### Critical Dependencies
- pygame: display and event handling
- math: basic mathematical calculations

### Identified Risks
- **Performance**: QuadTree/Barnes-Hut system may be complex to implement
- **Physics**: Inconsistent units may cause subtle bugs
- **Compatibility**: Relative display system must work on all resolutions

---

## Success Criteria

### February 2026
- ✅ All units are coherent and documented
- ✅ Display automatically adapts to any resolution
- ✅ Tests validated on 3+ different resolutions

### March 2026
- ✅ Partial collisions correctly transfer mass and energy
- ✅ Performance improved by at least 2x with 100+ bodies
- ✅ Energy and momentum conservation verified

### Q2 2026
- ✅ Complete and intuitive user interface
- ✅ Functional save system
- ✅ At least 3 predefined scenarios available

---

*Last updated: January 18, 2026*
*Author: Nils DONTOT*
