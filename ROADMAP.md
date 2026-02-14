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

### 🔄 February 2026 (In Progress - 50% Complete)
**Deadline: February 28, 2026**

#### ✅ Priority 1: Fixed Timestep Physics (COMPLETED)
- [x] Implemented fixed timestep integration (1/120s per step)
- [x] Added time accumulator system
- [x] Spiral of death prevention (max 250ms accumulation)
- [x] Deterministic physics regardless of rendering FPS
- [x] Separated physics_timestep from rendering FPS

#### ✅ Priority 2: Interpolated Rendering (COMPLETED)
- [x] Linear interpolation between physics states
- [x] Alpha blending for smooth 120 FPS visuals
- [x] Interpolated vector rendering (velocity + force)
- [x] Previous position tracking (prev_x, prev_y)
- [x] Smooth rendering even with variable frame rates

#### ✅ Priority 3: Code Organization (COMPLETED)
- [x] Created Color class for organized constants
- [x] Created Tester class with unit tests
  - [x] test_force_summation()
  - [x] test_determinism()
  - [x] test_uniform_speed()
  - [x] default_debug()
- [x] Improved force vector visualization (logarithmic scaling)
- [x] Multiple font support (main UI + splash screen)

#### 🔄 Priority 4: Unit System Coherence (IN PROGRESS)
- [x] Identified critical unit issues
  - [x] Density corrected: 5515 kg/m³ (was 5.515)
  - [x] Random field corrected: proper Joules conversion
  - [x] Velocity units identified: should be m/s (currently m/frame)
  - [x] Force averaging bug identified: should sum, not average
- [ ] **PENDING**: Full unit system correction
  - [ ] Fix velocity units from m/frame to m/s
  - [ ] Apply dt (delta time) in attract() method
  - [ ] Remove force averaging in update()
  - [ ] Simplify position update (remove correct_latency)
  - [ ] Document time_acceleration factor semantics
- [ ] **PENDING**: Scale factor system
  - [ ] Implement scale_factor (meters per pixel)
  - [ ] Choose appropriate scale (1e6 to 1e12)
  - [ ] Adjust minimum_mass for chosen scale
  - [ ] Convert all distance calculations
  - [ ] Convert rendering (radius, positions)
- [ ] Physical calculation validation tests

#### 📋 Priority 5: Relative Display System (PLANNED)
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

#### Priority 1: Complete Unit System Overhaul
- [ ] **Week 1-2**: Implement scale factor system
  - [ ] Add scale_factor to Engine.__init__()
  - [ ] Modify attract() for distance conversion
  - [ ] Modify update() for position conversion
  - [ ] Update draw_interpolated() for radius display
  - [ ] Test with various scale factors (1e6, 1e9, 1e12)
- [ ] **Week 2-3**: Fix velocity and force calculations
  - [ ] Apply dt in attract() method
  - [ ] Remove force averaging
  - [ ] Simplify position update
  - [ ] Add comprehensive unit tests
- [ ] **Week 3-4**: Documentation and validation
  - [ ] Create UNITS.md documentation
  - [ ] Test energy/momentum conservation
  - [ ] Verify physics accuracy with known scenarios

#### Priority 2: Partial Mass Transfer
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

#### Priority 3: Performance Optimization
- [ ] Research and design
  - [ ] Study QuadTree implementation
  - [ ] Analyze Barnes-Hut algorithm
  - [ ] Compare expected performance
- [ ] Implementation of chosen system
  - [ ] Optimized data structure
  - [ ] Spatial search algorithm
  - [ ] Optimized force calculations (reduce O(n²))
- [ ] Performance testing
  - [ ] Benchmarks with 10, 50, 100, 500 bodies
  - [ ] Before/after optimization comparison
  - [ ] Parameter tuning

#### Priority 4: Music System Completion
- [ ] Setup assets/musics/music*.mp3
- [ ] Test background music functionality
- [ ] Volume controls

---

## Q2 2026 (April - June)

### April 2026
**Deadline: April 30, 2026**

- [ ] Advanced camera system
  - [ ] Functional mouse wheel zoom
  - [ ] Smooth panning with mouse drag
  - [ ] Auto-follow selected body
  - [ ] Navigation mini-map
  - [ ] Reset view button

- [ ] Enhanced user interface
  - [ ] In-game settings menu
  - [ ] Simulation configuration panel
  - [ ] Configurable keyboard shortcuts
  - [ ] Vector scale controls
  - [ ] Time acceleration slider

### May 2026
**Deadline: May 31, 2026**

- [ ] Save/Load system
  - [ ] Export simulation to JSON
    - [ ] Serialize all Circle properties
    - [ ] Serialize Engine settings
    - [ ] Include metadata (version, date, author)
  - [ ] Import simulation
    - [ ] Validate JSON structure
    - [ ] Handle version compatibility
    - [ ] Error handling for corrupted files
  - [ ] Auto-save functionality
    - [ ] Periodic auto-save (configurable interval)
    - [ ] Recovery from crashes
  - [ ] Scenario preset management
    - [ ] Built-in presets library
    - [ ] User custom presets

- [ ] Predefined simulation scenarios
  - [ ] Solar system (Sun + 8 planets)
  - [ ] Binary star system
  - [ ] Triple star system
  - [ ] Stellar cluster (50+ stars)
  - [ ] Galaxy collision
  - [ ] Accretion disk

### June 2026
**Deadline: June 30, 2026**

- [ ] Performance improvements
  - [ ] Code profiling with cProfile
  - [ ] Critical loop optimization
  - [ ] Consider NumPy for vectorized calculations
  - [ ] Investigate Cython for hot paths
  - [ ] Multi-threading for force calculations (if beneficial)

- [ ] Configuration system
  - [ ] External config file (JSON/YAML)
  - [ ] Runtime parameter adjustment
  - [ ] User preferences persistence

---

## Q3 2026 (July - September)

### July 2026

- [ ] Advanced visual effects
  - [ ] Motion trails with fade-out
  - [ ] Enhanced collision effects (particles, flashes)
  - [ ] Reference grid overlay
  - [ ] Predicted trajectory display (orbital paths)
  - [ ] Body glow effects (brightness based on mass)

### August 2026

- [ ] Analysis tools
  - [ ] Real-time graphs (Matplotlib integration)
    - [ ] Total energy over time
    - [ ] Total momentum over time
    - [ ] Angular momentum
  - [ ] Statistics dashboard
    - [ ] Average velocity
    - [ ] Total collisions
    - [ ] Fusion events
  - [ ] Data export
    - [ ] CSV export for analysis
    - [ ] Screenshot capture
    - [ ] Video recording (optional)

### September 2026

- [ ] Complete documentation
  - [ ] User guide (PDF/Markdown)
    - [ ] Getting started
    - [ ] Controls reference
    - [ ] Configuration guide
    - [ ] Troubleshooting
  - [ ] API documentation (Sphinx)
    - [ ] All classes documented
    - [ ] Method signatures
    - [ ] Usage examples
  - [ ] Video tutorials
    - [ ] Basic usage
    - [ ] Creating scenarios
    - [ ] Understanding physics
  - [ ] Interactive tutorial mode
    - [ ] Step-by-step guide in-app
    - [ ] Tooltips and hints

---

## Q4 2026 (October - December)

### October - December 2026

- [ ] Advanced features
  - [ ] Scenario editor
    - [ ] Graphical body placement
    - [ ] Velocity vector editor
    - [ ] Parameter tweaking
  - [ ] Challenges/puzzles mode
    - [ ] Achieve stable orbits
    - [ ] Minimize collisions
    - [ ] Time-limited scenarios
  - [ ] Replay system
    - [ ] Record simulations
    - [ ] Playback with speed control
    - [ ] Save replays to file

- [ ] Polish and refinement
  - [ ] UI/UX improvements
  - [ ] Performance final optimization
  - [ ] Bug fixes
  - [ ] User feedback integration

---

## Backlog (2027+)

### Major Features
- [ ] **GPU Acceleration** (Q1 2027)
  - Support thousands of bodies simultaneously
  - CUDA/OpenCL implementation
  - 10-100× performance improvement
  - Options: CuPy, PyCUDA, PyOpenCL, Taichi

- [ ] **3D Mode** (Q2-Q3 2027)
  - Three-dimensional simulation
  - Rotating 3D camera (mouse controls)
  - OpenGL/Vulkan rendering
  - Shader-based lighting
  - Depth perception (fog, shadows)

- [ ] **Advanced Physics** (Q4 2027)
  - Body deformation (tidal forces)
  - Fragmentation on violent collisions
  - Black hole physics
    - Event horizon visualization
    - Accretion disk
    - Hawking radiation (simplified)
  - Simplified general relativity effects
    - Gravitational lensing
    - Time dilation near massive objects

### Community Features
- [ ] **Network/Multiplayer** (2028)
  - Collaborative simulations
  - Online scenario sharing platform
  - Community leaderboards
  - Challenge mode

- [ ] **AI/ML Integration** (2028)
  - Trajectory prediction (neural network)
  - Automatic parameter optimization
  - Procedural generation of stable systems
  - Pattern recognition (stable vs chaotic)

### Technical Improvements
- [ ] Comprehensive unit tests (pytest)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Packaging
  - [ ] PyPI distribution
  - [ ] Improved standalone executables
  - [ ] Installers (Windows MSI, macOS DMG)
- [ ] Native multi-platform support
  - [ ] macOS optimizations
  - [ ] Linux optimizations
  - [ ] Cross-platform builds

---

## Recent Achievements (February 2026)

### ✨ Major Accomplishments
1. **Fixed Timestep Physics** - Simulation is now deterministic and FPS-independent
2. **Interpolated Rendering** - Smooth 120 FPS visuals with alpha blending
3. **Code Quality** - Organized Color/Tester classes, unit tests
4. **Physics Improvements** - Better force vector visualization
5. **Documentation** - Comprehensive code comments and docstrings

### 🎯 Key Metrics
- **Code Quality**: Improved from ~70% to ~90% documentation coverage
- **Physics Accuracy**: Fixed timestep ensures consistent simulation
- **Performance**: Stable 120 FPS with proper interpolation
- **Testability**: 3 unit tests for physics validation

---

## Development Notes

### Current Technical State
- **Physics**: Fixed timestep (1/120s), interpolated rendering ✅
- **Performance**: O(n²) calculations, ~50-100 bodies smoothly
- **Display**: 2D, Pygame-based, fullscreen/windowed
- **Architecture**: Modular classes, organized structure

### Critical Dependencies
- **pygame 2.0+**: Display and event handling
- **Python 3.11+**: Type hints, match statements
- **Standard library**: math, time, random, os, sys

### Technical Debt Identified
1. **Unit System** (HIGH PRIORITY)
   - Velocity in m/frame instead of m/s
   - Force averaging instead of summation
   - No scale factor (1 pixel = 1 meter is absurd)
   - Position update uses confusing correct_latency()

2. **Code Organization** (MEDIUM PRIORITY)
   - Global engine instance (not ideal)
   - Circular dependencies (engine ↔ Circle)
   - Some debug prints left in code

3. **Performance** (MEDIUM PRIORITY)
   - O(n²) force calculations
   - No spatial partitioning
   - Single-threaded

### Identified Risks
- **Performance**: QuadTree/Barnes-Hut system complex to implement
- **Physics**: Unit inconsistencies may cause subtle bugs
- **Scale**: Large mass differences can cause numerical instability
- **Compatibility**: Must test on various resolutions

---

## Success Criteria

### ✅ February 2026 (ACHIEVED)
- [x] Fixed timestep physics implemented and tested
- [x] Interpolation provides smooth 120 FPS rendering
- [x] Unit tests validate determinism and consistency
- [x] Code organization improved (Color, Tester classes)
- [x] Force vectors correctly preserve direction

### 🎯 March 2026 (TARGET)
- [ ] All units coherent and documented (UNITS.md)
- [ ] Scale factor system implemented and tested
- [ ] Velocity in m/s throughout codebase
- [ ] Force summation corrected
- [ ] Energy/momentum conservation validated
- [ ] Performance improved 2× (QuadTree or spatial hashing)

### 🎯 Q2 2026 (TARGET)
- [ ] Complete and intuitive user interface
- [ ] Functional save/load system
- [ ] At least 5 predefined scenarios available
- [ ] Camera system with zoom/pan
- [ ] Configuration file system

### 🎯 Q3 2026 (TARGET)
- [ ] Advanced visual effects (trails, particles)
- [ ] Analysis tools with real-time graphs
- [ ] Complete documentation (guide + API)
- [ ] Video tutorials published
- [ ] User testing and feedback integration

---

## Contributing

### How to Contribute
1. Check the roadmap for planned features
2. Pick an item from backlog or current priorities
3. Create an issue or comment on existing ones
4. Submit pull request with:
   - Clear description of changes
   - Tests if applicable
   - Updated documentation

### Priority Areas for Help
- 🔴 **HIGH**: Unit system corrections (March 2026)
- 🟡 **MEDIUM**: QuadTree implementation (March 2026)
- 🟡 **MEDIUM**: Save/load system (May 2026)
- 🟢 **LOW**: Predefined scenarios (May 2026)
- 🟢 **LOW**: Visual effects (July 2026)

---

## Version History

### v2.0.0 - Fixed Timestep Edition (February 14, 2026)
- Added fixed timestep physics integration
- Added interpolated rendering system
- Added Color class for organization
- Added Tester class with unit tests
- Improved force vector visualization
- Multiple font support

### v1.0.0 - Initial Release (January 2026)
- Basic N-body simulation
- Real-time gravitational calculations
- Body creation and fusion
- Vector visualization
- Random modes
- Splash screen

---

*Last updated: February 14, 2026*  
*Author: Nils DONTOT*  
*Current Version: 2.0.0 - Fixed Timestep Edition*
