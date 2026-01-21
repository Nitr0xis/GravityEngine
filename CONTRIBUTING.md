# Contributing to Gravity Engine

First off, thank you for considering contributing to Gravity Engine! 🎉

It's people like you that make Gravity Engine such a great tool for learning and exploring physics simulations.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Coding Standards](#-coding-standards)
- [Physics Guidelines](#-physics-guidelines)
- [Commit Guidelines](#-commit-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Community](#-community)

---

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a friendly, safe, and welcoming environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Age
- Sexual orientation
- Disability
- Personal appearance
- Race or ethnicity
- Religion or lack thereof
- Nationality

### Our Standards

**Examples of behavior that contributes to a positive environment:**

✅ Using welcoming and inclusive language  
✅ Being respectful of differing viewpoints and experiences  
✅ Gracefully accepting constructive criticism  
✅ Focusing on what is best for the community  
✅ Showing empathy towards other community members  

**Examples of unacceptable behavior:**

❌ Trolling, insulting/derogatory comments, and personal or political attacks  
❌ Public or private harassment  
❌ Publishing others' private information without explicit permission  
❌ Other conduct which could reasonably be considered inappropriate  

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project maintainer at [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com). All complaints will be reviewed and investigated promptly and fairly.

---

## 🤝 How Can I Contribute?

### 1. Reporting Bugs 🐛

**Before submitting a bug report:**
- Check the [existing issues](https://github.com/Nitr0xis/GravityEngine/issues) to avoid duplicates
- Try to reproduce the bug with the latest version
- Collect relevant information (OS, Python version, error messages)

**How to submit a good bug report:**

Create an issue with the following template:
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Create body with '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows 10, macOS 12, Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - Pygame Version: [e.g. 2.5.0]
 - Running from: [Source / Executable]

**Additional context**
Add any other context about the problem here.
```

### 2. Suggesting Enhancements 💡

**Before submitting an enhancement:**
- Check if it's already suggested in [issues](https://github.com/Nitr0xis/GravityEngine/issues)
- Check the [ROADMAP.md](ROADMAP.md) to see if it's already planned
- Consider if it fits the project's scope

**How to submit a good enhancement suggestion:**
```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Physics/technical considerations**
If applicable, explain the physics or technical approach.

**Additional context**
Add any other context, mockups, or screenshots about the feature request.
```

### 3. Contributing Code 💻

We welcome code contributions! Here are areas that need help:

#### High Priority
- 🐛 **Bug fixes** - Stability improvements
- ⚡ **Performance optimizations** - Especially O(n²) algorithm improvements
- 📊 **Physics accuracy** - Improving calculations and formulas
- 🎨 **UI/UX improvements** - Better user interface

#### Medium Priority
- 🔧 **New features** from [ROADMAP.md](ROADMAP.md)
- 📖 **Documentation** - Code comments, docstrings, tutorials
- 🧪 **Testing** - Unit tests, integration tests
- 🌍 **Internationalization** - Multi-language support

#### Nice to Have
- 🎮 **New simulation modes** - Different scenarios
- 📊 **Data export** - Save simulation data
- 🎨 **Visual effects** - Trails, better rendering
- 🔊 **Audio** - Background music system

---

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/GravityEngine.git
cd GravityEngine
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install pygame

# Optional: Install development tools
pip install pylint black pytest
```

### 3. Create a Branch
```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Examples:
git checkout -b fix/collision-bug
git checkout -b feature/quadtree-optimization
git checkout -b docs/improve-readme
```

### 4. Make Your Changes

Edit files in your preferred editor:
- Main code: `src/gravity_engine.py`
- Documentation: `README.md`, `ROADMAP.md`
- Build scripts: `builders/*.bat`

### 5. Test Your Changes
```bash
# Run the program
python src/gravity_engine.py

# Test different scenarios:
# - Create many bodies (performance test)
# - Test fusion mechanics
# - Test vector visualization
# - Test pause/resume
# - Test random mode
```

---

## 🔄 Development Workflow

### Recommended Workflow

1. **Check issues** - See if your idea/bug is already tracked
2. **Create issue** (optional) - Discuss larger changes first
3. **Fork & branch** - Create your feature branch
4. **Code** - Make your changes following our standards
5. **Test** - Verify everything works
6. **Commit** - Use clear, descriptive commit messages
7. **Push** - Push to your fork
8. **Pull Request** - Submit PR with detailed description

### Development Tips

- **Test frequently** - Run the simulation after each change
- **Small commits** - Make atomic commits (one logical change per commit)
- **Ask questions** - Open an issue if you need help
- **Stay updated** - Regularly pull from upstream main

---

## 📏 Coding Standards

### Python Style Guide (PEP 8)

We follow [PEP 8](https://pep8.org/) with some flexibility:
```python
# ✅ GOOD
def calculate_gravitational_force(mass1: float, mass2: float, distance: float) -> float:
    """
    Calculate gravitational force between two bodies.
    
    Args:
        mass1: Mass of first body in kg
        mass2: Mass of second body in kg
        distance: Distance between bodies in meters
    
    Returns:
        Gravitational force in Newtons
    """
    G = 6.6743e-11  # Gravitational constant
    if distance == 0:
        return 0
    return G * (mass1 * mass2) / (distance ** 2)


# ❌ BAD
def calc_force(m1,m2,d):
    return 6.6743e-11*(m1*m2)/(d**2)
```

### Code Organization
```python
# ✅ GOOD - Organized sections with clear comments

# -----------------
# class Circle
# -----------------
class Circle:
    def __init__(self, x, y, radius, mass):
        """Initialize a gravitational body."""
        # Position
        self.x = float(x)
        self.y = float(y)
        
        # Physical properties
        self.mass = mass
        self.radius = radius
        
        # Velocity
        self.vx = 0
        self.vy = 0


# ❌ BAD - No organization or comments
class Circle:
    def __init__(self,x,y,radius,mass):
        self.x=float(x)
        self.y=float(y)
        self.mass=mass
        self.radius=radius
        self.vx=0
        self.vy=0
```

### Naming Conventions
```python
# Classes - PascalCase
class GravityEngine:
    pass

# Functions/Methods - snake_case
def calculate_distance(x1, y1, x2, y2):
    pass

# Constants - UPPER_SNAKE_CASE
GRAVITATIONAL_CONSTANT = 6.6743e-11
MAX_BODIES = 1000

# Variables - snake_case
total_mass = 0
body_count = len(circles)

# Private attributes - _leading_underscore
self._internal_state = None
```

### Comments and Docstrings
```python
# ✅ GOOD - Comprehensive docstrings

def attract(self, other, effective: bool = True) -> tuple[float, float]:
    """
    Calculate gravitational attraction with another body.
    
    Uses Newton's law of universal gravitation:
    F = G * (m1 * m2) / r²
    
    Args:
        other: The other Circle to calculate attraction with
        effective: If True, apply the force to update velocity
    
    Returns:
        tuple: (fx, fy) - Force components in x and y directions (Newtons)
    
    Note:
        Returns (0, 0) if bodies are colliding (distance <= sum of radii)
    """
    # Calculate distance vector
    dx = other.x - self.x
    dy = other.y - self.y
    distance = sqrt(dx**2 + dy**2)
    
    # Check for collision
    if distance <= self.radius + other.radius:
        return 0, 0
    
    # Calculate force magnitude
    force = self.G * (self.mass * other.mass) / (distance**2)
    
    # Convert to force vector
    angle = atan2(dy, dx)
    fx = cos(angle) * force
    fy = sin(angle) * force
    
    return fx, fy


# ❌ BAD - No docstring, unclear comments
def attract(self,other,effective=True):
    #calc force
    dx=other.x-self.x
    dy=other.y-self.y
    d=sqrt(dx**2+dy**2)
    if d<=self.radius+other.radius:return 0,0
    f=self.G*(self.mass*other.mass)/(d**2)
    a=atan2(dy,dx)
    return cos(a)*f,sin(a)*f
```

### Type Hints

Use type hints for better code clarity:
```python
# ✅ GOOD
def fusion(self, other: 'Circle') -> None:
    """Merge two bodies conserving momentum."""
    total_mass: float = self.mass + other.mass
    self.x = (self.x * self.mass + other.x * other.mass) / total_mass

# ✅ ALSO GOOD
def get_nearest(self) -> tuple[int, float] | None:
    """Find nearest body."""
    if len(circles) == 0:
        return None
    return body_id, distance
```

---

## 🔬 Physics Guidelines

### Physical Accuracy

When contributing physics-related code:

1. **Use correct formulas**
```python
   # ✅ CORRECT - Newton's law
   force = G * (m1 * m2) / (distance ** 2)
   
   # ❌ WRONG - Don't invent physics
   force = G * (m1 + m2) / distance
```

2. **Preserve conservation laws**
   - Momentum must be conserved in collisions
   - Energy should be tracked (even if not perfectly conserved due to numerical errors)
   - Angular momentum (when applicable)

3. **Use SI units consistently**
```python
   # Masses in kilograms (or tonnes)
   # Distances in meters
   # Time in seconds
   # Forces in Newtons
   # Energies in Joules
```

4. **Document physics assumptions**
```python
   # ✅ GOOD
   def fusion(self, other):
       """
       Merge two bodies using perfectly inelastic collision.
       
       Assumptions:
       - Perfect momentum conservation
       - No energy loss (unrealistic but simplifies simulation)
       - Spherical bodies with uniform density
       - Instantaneous collision (no deformation time)
       """
```

### Numerical Stability
```python
# ✅ GOOD - Check for division by zero
if distance > 0:
    force = G * (m1 * m2) / (distance ** 2)
else:
    force = 0

# ✅ GOOD - Prevent extreme values
max_force = 1e10  # Maximum force cap
force = min(calculated_force, max_force)

# ✅ GOOD - Handle edge cases
if self.mass == 0:
    return  # Massless body doesn't attract
```

---

## 📝 Commit Guidelines

### Commit Message Format

Use clear, descriptive commit messages:
```
<type>: <subject>

[optional body]

[optional footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring (no feature change)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system changes
- **chore**: Maintenance tasks

### Examples
```bash
# ✅ GOOD commits
git commit -m "feat: add QuadTree spatial partitioning for O(n log n) complexity"
git commit -m "fix: correct momentum conservation in fusion calculation"
git commit -m "docs: add physics formulas to README"
git commit -m "perf: optimize force calculation loop by 40%"
git commit -m "refactor: reorganize Engine.__init__() into logical sections"

# ❌ BAD commits
git commit -m "fixed stuff"
git commit -m "update"
git commit -m "wip"
git commit -m "asdf"
```

### Detailed Commit Messages

For complex changes:
```bash
git commit -m "feat: implement Barnes-Hut algorithm for gravitational calculations

- Replace O(n²) brute force with O(n log n) tree-based approach
- Add QuadTree data structure for spatial partitioning
- Implement theta approximation parameter (default: 0.5)
- Performance improvement: 10x faster with 1000+ bodies
- Maintains physics accuracy within 1% of exact calculation

Resolves #42"
```

---

## 🔀 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines (PEP 8)
- [ ] All functions have docstrings
- [ ] Physics is accurate (formulas verified)
- [ ] Code has been tested manually
- [ ] No debug print() statements left in code
- [ ] Commit messages are clear and descriptive
- [ ] README/docs updated (if needed)

### PR Template

When creating a pull request, include:
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Changes Made
- List specific changes made
- Be concise but informative
- Use bullet points

## Testing Done
- Describe how you tested your changes
- List test scenarios
- Include screenshots/videos if applicable

## Physics Verification (if applicable)
- Formulas used and their sources
- Conservation laws verified
- Numerical stability checks

## Related Issues
Closes #(issue number)

## Screenshots
If applicable, add screenshots showing the changes.

## Additional Notes
Any additional context or notes for reviewers.
```

### Review Process

1. **Automated checks** - GitHub Actions (if configured)
2. **Code review** - Maintainer reviews code quality
3. **Physics review** - Verify physical accuracy
4. **Testing** - Manual testing by maintainer
5. **Approval** - PR approved and merged
6. **Acknowledgment** - You're added to contributors! 🎉

### What to Expect

- **Response time**: Usually within 2-7 days
- **Feedback**: Constructive suggestions for improvement
- **Iteration**: You may be asked to make changes
- **Patience**: Remember, this is maintained by a 15-year-old student! 😊

---

## 🧪 Testing

### Manual Testing Checklist

When testing your changes, verify:

#### Basic Functionality
- [ ] Program starts without errors
- [ ] Can create bodies with mouse
- [ ] Bodies move and attract each other
- [ ] Pause/resume works
- [ ] Can select and delete bodies

#### Physics Accuracy
- [ ] Two-body orbit is stable
- [ ] Momentum is conserved in collisions
- [ ] Bodies don't accelerate spontaneously
- [ ] Fusion produces correct mass

#### Performance
- [ ] No significant FPS drop with <100 bodies
- [ ] No memory leaks during long simulations
- [ ] Vectors render without lag

#### Edge Cases
- [ ] Zero-mass bodies handled correctly
- [ ] Overlapping bodies at creation
- [ ] Very large/small bodies
- [ ] Extreme time acceleration

### Automated Testing (Future)

We plan to add:
- Unit tests for physics calculations
- Integration tests for core features
- Performance benchmarks
- Continuous integration

---

## 📖 Documentation

### Code Documentation

Every function should have a docstring:
```python
def calculate_energy(self) -> float:
    """
    Calculate total kinetic energy of the body.
    
    Uses the formula: E = (1/2) * m * v²
    
    Returns:
        float: Kinetic energy in Joules
    
    Note:
        Energy is calculated in the instantaneous reference frame
    """
    velocity = sqrt(self.vx**2 + self.vy**2)
    return 0.5 * self.mass * (velocity ** 2)
```

### README Updates

If your change affects user-facing features:

1. Update relevant section in README.md
2. Add to feature list if it's a new feature
3. Update configuration examples if needed
4. Add to roadmap if partially implemented

### Changelog

Significant changes should be noted in ROADMAP.md:
```markdown
### January 2026
- [x] Added QuadTree optimization (PR #45)
- [x] Fixed momentum conservation bug (PR #43)
- [x] Improved UI responsiveness (PR #47)
```

---

## 👥 Community

### Getting Help

- **Questions**: Open an issue with the `question` label
- **Discussion**: Use GitHub Discussions (if enabled)
- **Email**: Contact [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)

### Recognition

Contributors are acknowledged in:
- README.md (Contributors section)
- Release notes
- Commit history

### Collaboration

- Be patient and respectful
- Help others when you can
- Share your knowledge
- Learn from feedback

---

## 🎓 Learning Resources

### Physics
- [Newton's Law of Universal Gravitation](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation)
- [N-body Problem](https://en.wikipedia.org/wiki/N-body_problem)
- [Momentum Conservation](https://en.wikipedia.org/wiki/Momentum#Conservation)

### Programming
- [Python PEP 8 Style Guide](https://pep8.org/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

### Algorithms
- [QuadTree Data Structure](https://en.wikipedia.org/wiki/Quadtree)
- [Barnes-Hut Algorithm](https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation)

---

## 🏆 Recognition

### Hall of Contributors

Thank you to all contributors who help make Gravity Engine better!

<!-- This section will be updated as contributors join -->

**Core Contributors:**
- Nils DONTOT ([@Nitr0xis](https://github.com/Nitr0xis)) - Creator and maintainer

**Contributors:**
- *Your name could be here!* 🌟

---

## 📋 Quick Reference

### Common Tasks
```bash
# Set up development environment
git clone https://github.com/YOUR_USERNAME/GravityEngine.git
cd GravityEngine
python -m venv venv
venv\Scripts\activate  # Windows
pip install pygame

# Create feature branch
git checkout -b feature/my-feature

# Make changes, then:
git add .
git commit -m "feat: description of changes"
git push origin feature/my-feature

# Then create PR on GitHub
```

### Need Help?

- 📖 Read the [README.md](README.md)
- 🗺️ Check [ROADMAP.md](ROADMAP.md)
- 🐛 Search [existing issues](https://github.com/Nitr0xis/GravityEngine/issues)
- 📧 Email: [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)

---

## 🙏 Thank You!

Thank you for taking the time to contribute to Gravity Engine! Every contribution, no matter how small, helps make this project better for everyone.

**Happy coding, and may gravity be with you!** 🌌✨

---

*Last updated: January 21, 2026*
*Maintained by Nils DONTOT*
