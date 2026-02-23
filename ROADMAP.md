# Roadmap - Gravity Engine

## Overview
This document outlines the development roadmap for Gravity Engine with prioritized objectives and their deadlines.

---

## Q1 2026 (January - March)

### January 2026 (Completed)
- [x] Fixed collision detection for recently created circles
- [x] Implemented temporary text system (TempText)
- [x] Improved fullscreen display mode management
- [x] Collision detection by distance rather than rect

### February 2026 (COMPLETED - 100%)
**Completed: February 23, 2026**

#### Priority 1: Fixed Timestep Physics (COMPLETED)
- [x] Implemented fixed timestep integration (1/120s per step)
- [x] Added time accumulator system
- [x] Spiral of death prevention (max 250ms accumulation)
- [x] Deterministic physics regardless of rendering FPS
- [x] Separated physics_timestep from rendering FPS

#### Priority 2: Interpolated Rendering - Mode PRECISE (COMPLETED)
- [x] Linear interpolation between physics states
- [x] Alpha blending for smooth 120 FPS visuals
- [x] **Position interpolation** (prev_x, prev_y)
- [x] **Velocity interpolation** (prev_vx, prev_vy)
- [x] **Force interpolation** (prev_force)
- [x] **Radius interpolation** (prev_radius for smooth fusions)
- [x] **Interpolation cache** (avoid redundant calculations)
- [x] Interpolated vector rendering (velocity + force)
- [x] Smooth rendering even with variable frame rates

#### Priority 3: Code Organization (COMPLETED)
- [x] Created Color class for organized constants
- [x] Created Tester class with unit tests
  - [x] test_force_summation()
  - [x] test_determinism()
  - [x] test_uniform_speed()
  - [x] test_position_interpolation()
  - [x] test_velocity_interpolation()
  - [x] test_force_interpolation()
  - [x] test_interpolation_cache()
  - [x] default_debug()
- [x] Improved force vector visualization (logarithmic scaling)
- [x] Multiple font support (main UI + splash screen)

#### Priority 4: Adaptive Performance Mode (COMPLETED)
- [x] Implemented adaptive throttling system
  - [x] Configurable physics update frequency (min_physics_interval)
  - [x] Default: 40 Hz physics (25ms between updates)
  - [x] Automatic CPU load management
  - [x] Smooth 120 FPS rendering regardless of body count
- [x] Visual collision detection
  - [x] Detect collisions on interpolated positions
  - [x] Force immediate physics calculation on visual collision
  - [x] Prevent "bodies passing through" visually
  - [x] Seamless integration with interpolation system
- [x] Interpolated click detection
  - [x] Mouse click detection on visual positions
  - [x] Select bodies where you see them
  - [x] More intuitive user experience
- [x] Performance mode configuration
  - [x] "precise" mode: Fixed 120 Hz physics (high accuracy)
  - [x] "adaptive" mode: Throttled physics (smooth rendering)
  - [x] Easy switching between modes
  - [x] Comprehensive documentation

#### Priority 5: Unit System Coherence (IN PROGRESS - 30%)
- [x] Identified critical unit issues
  - [x] Density corrected: 5514 kg/m³ (was 5.515)
  - [x] Random field corrected: proper Joules conversion
  - [x] Velocity units identified: should be m/s
  - [x] Force summation corrected (no more averaging)
- [ ] **IN PROGRESS**: Full unit system implementation
  - [x] Velocity units properly in m/s
  - [x] Force summation implemented
  - [x] Position update simplified (dt_sim application)
  - [ ] Scale factor system (1 pixel ≠ 1 meter)
  - [ ] Document time_acceleration factor semantics
- [ ] **PENDING**: Scale factor system
  - [ ] Implement scale_factor (meters per pixel)
  - [ ] Choose appropriate scale (1e6 to 1e12)
  - [ ] Adjust minimum_mass for chosen scale
  - [ ] Convert all distance calculations
  - [ ] Convert rendering (radius, positions)
- [ ] Physical calculation validation tests

### March 2026 (In Progress - 15% Complete)
**Deadline: March 31, 2026**

#### Priority 1: Complete Unit System Overhaul (Week 1-2)
- [ ] **Scale factor system implementation**
  - [ ] Add scale_factor to Engine.__init__()
  - [ ] Modify attract() for distance conversion
  - [ ] Modify update() for position conversion
  - [ ] Update draw_interpolated() for radius display
  - [ ] Test with various scale factors (1e6, 1e9, 1e12)
- [ ] **Documentation and validation**
  - [ ] Create UNITS.md documentation
  - [ ] Test energy/momentum conservation
  - [ ] Verify physics accuracy with known scenarios
  - [ ] Add unit conversion reference table

#### Priority 2: Enhanced Interpolation System (Week 2-3)
- [ ] **Adaptive interpolation mode**
  - [ ] Implement Hermite cubic interpolation
  - [ ] Implement Catmull-Rom interpolation
  - [ ] Add configuration: "precise" vs "adaptive" interpolation
  - [ ] Performance comparison tests
- [ ] **Advanced interpolation features**
  - [ ] Acceleration interpolation (optional)
  - [ ] Rotation interpolation (for future 3D)
  - [ ] Color interpolation (for future visual effects)
  - [ ] Optimized interpolation for large simulations

#### Priority 3: Partial Mass Transfer (Week 3)
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

#### Priority 4: Performance Optimization (Week 4)
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

#### Priority 5: Music System Completion
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
  - [ ] Performance mode selector
  - [ ] Interpolation mode selector

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
  - 10-100x performance improvement
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

## Recent Achievements (February 2026 - v3.1.0)

### Major Accomplishments
1. **Complete Mode PRECISE Interpolation** - Position, velocity, force, radius fully interpolated
   - Velocity vectors now perfectly smooth
   - Force vectors transition smoothly
   - Radius grows progressively during fusions
   - Interpolation cache prevents redundant calculations
   - 7 new unit tests for interpolation validation
2. **Adaptive Performance Mode** - Intelligent throttling for smooth 120 FPS
   - Configurable physics update frequency (default 40 Hz)
   - Automatic CPU load management
   - Smooth rendering with 100+ bodies
   - Easy switching between "precise" and "adaptive" modes
3. **Visual Collision Detection** - Collisions on what you see, not just physics
   - Detects collisions on interpolated positions
   - Forces immediate physics calculation when needed
   - Prevents visual "pass-through" artifacts
4. **Interpolated Click Detection** - Select bodies where you see them
   - Mouse click uses visual positions, not physical
   - More intuitive user experience
   - Perfect integration with interpolation
5. **Fixed Timestep Physics** - Simulation is now deterministic and FPS-independent
6. **Code Quality** - Organized Color/Tester classes, comprehensive unit tests
7. **Physics Improvements** - Better force vector visualization, proper unit handling

### Key Metrics
- **Performance**: 100+ bodies at smooth 120 FPS (adaptive mode)
- **Accuracy**: Fixed timestep ensures consistent simulation (precise mode)
- **Code Quality**: ~95% documentation coverage
- **User Experience**: Complete interpolation + visual collision detection
- **Testability**: 7 unit tests for physics and interpolation validation

### Version 3.1.0 Highlights
```
NEW: Complete Mode PRECISE interpolation (position, velocity, force, radius)
NEW: Interpolation cache for performance
NEW: 4 additional unit tests for interpolation
IMPROVED: Velocity vectors perfectly smooth (interpolated vx, vy)
IMPROVED: Force vectors transition smoothly (interpolated fx, fy)
IMPROVED: Fusions visually smooth (interpolated radius)
IMPROVED: Comprehensive testing framework
```

---

## Development Notes

### Current Technical State (v3.1.0)
- **Physics**: Fixed timestep (1/120s) OR adaptive throttling (40 Hz)
- **Rendering**: Fully interpolated 120 FPS (position, velocity, force, radius)
- **Collision**: Visual detection on interpolated positions
- **Performance**: O(n²) calculations, ~100+ bodies smoothly (adaptive)
- **Display**: 2D, Pygame-based, fullscreen/windowed
- **Architecture**: Modular classes, organized structure
- **Testing**: 7 unit tests (force, determinism, speed, interpolation×4)

### Critical Dependencies
- **pygame 2.0+**: Display and event handling
- **Python 3.11+**: Type hints, match statements
- **Standard library**: math, time, random, os, sys

### Technical Debt Identified
1. **Scale Factor System** (HIGH PRIORITY - Next step)
   - 1 pixel = 1 meter is unrealistic
   - Need scale factor (e.g., 1 pixel = 1e6 meters)
   - Affects distance calculations and rendering
   - Minimum mass needs adjustment for chosen scale

2. **Unit System Documentation** (MEDIUM PRIORITY)
   - Time acceleration semantics unclear
   - Need comprehensive UNITS.md
   - Unit conversion reference table

3. **Code Organization** (LOW PRIORITY)
   - Global engine instance (acceptable for now)
   - Circular dependencies (engine ↔ Circle)
   - Some debug code could be cleaned

4. **Performance** (LOW PRIORITY - Adaptive mode helps)
   - O(n²) force calculations (acceptable with adaptive mode)
   - No spatial partitioning (planned for March)
   - Single-threaded (acceptable performance)

### Identified Risks
- **Scale factor**: Requires careful testing with different scales
- **Physics accuracy**: Adaptive mode trades accuracy for smoothness
- **Numerical stability**: Large mass differences can cause issues
- **Compatibility**: Must test on various resolutions

---

## Success Criteria

### February 2026 (ACHIEVED - v3.1.0)
- [x] Fixed timestep physics implemented and tested
- [x] Complete interpolation system (position, velocity, force, radius)
- [x] Interpolation cache for performance optimization
- [x] Unit tests validate physics and interpolation
- [x] Code organization improved (Color, Tester classes)
- [x] Force vectors correctly preserve direction
- [x] Adaptive performance mode implemented
- [x] Visual collision detection working
- [x] Interpolated click detection functional
- [x] Smooth 120 FPS with 100+ bodies
- [x] Velocity and force vectors perfectly smooth
- [x] Fusion radius transitions smoothly

### March 2026 (TARGET - Week 1-2)
- [ ] Scale factor system implemented and tested
- [ ] UNITS.md documentation complete
- [ ] All units coherent and validated
- [ ] Energy/momentum conservation verified
- [ ] Adaptive interpolation mode (Hermite) implemented
- [ ] Performance improved 2x (QuadTree or spatial hashing)

### Q2 2026 (TARGET)
- [ ] Complete and intuitive user interface
- [ ] Functional save/load system
- [ ] At least 5 predefined scenarios available
- [ ] Camera system with zoom/pan
- [ ] Configuration file system

### Q3 2026 (TARGET)
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
- HIGH: Scale factor system (March 2026 - Week 1-2)
- MEDIUM: Adaptive interpolation mode (March 2026 - Week 2-3)
- MEDIUM: QuadTree implementation (March 2026 - Week 4)
- MEDIUM: Save/load system (May 2026)
- LOW: Predefined scenarios (May 2026)
- LOW: Visual effects (July 2026)

---

## Version History

### v3.1.0 - Complete PRECISE Interpolation (February 23, 2026)
**Major Features:**
- Complete Mode PRECISE interpolation (position, velocity, force, radius)
- Interpolation cache system for performance
- 4 new unit tests for interpolation validation
- Perfectly smooth velocity and force vectors
- Progressive radius growth during fusions

**Improvements:**
- Velocity interpolation (prev_vx, prev_vy)
- Force interpolation (prev_force)
- Radius interpolation (prev_radius)
- Cache invalidation system
- Comprehensive get_interpolated_state() method

**Technical:**
- Interpolation cache with alpha validation
- .copy() for force lists to prevent reference issues
- Initialization of prev_vx/vy in random mode
- Cache invalidation on physics_update() and fusion()
- 7 total unit tests (3 physics + 4 interpolation)

### v3.0.0 - Adaptive Performance Edition (February 19, 2026)
**Major Features:**
- Added adaptive performance mode with throttling (40 Hz physics by default)
- Added visual collision detection on interpolated positions
- Added interpolated click detection for body selection
- Configurable performance modes: "precise" vs "adaptive"
- Smooth 120 FPS rendering with 100+ bodies in adaptive mode

**Improvements:**
- Better user experience with visual collision detection
- More intuitive click detection on visual positions
- Comprehensive documentation for new features
- Performance improvements for large simulations

**Technical:**
- min_physics_interval configuration
- last_physics_time tracking
- physics_time_debt accumulation
- Visual collision forcing immediate physics step
- Skip prev_update flag for smooth transitions

### v2.0.0 - Fixed Timestep Edition (February 14, 2026)
- Added fixed timestep physics integration
- Added interpolated rendering system (position only)
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

*Last updated: February 23, 2026*  
*Author: Nils DONTOT*  
*Current Version: 3.1.0 - Complete PRECISE Interpolation*
