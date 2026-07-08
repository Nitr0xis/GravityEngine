# Contributing to GravityEngine

Thanks for considering a contribution. This document covers how to report bugs, suggest features, and submit code.

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

---

## Table of Contents

- [How to Contribute](#how-to-contribute)
- [Getting Started](#getting-started)
- [Coding Standards](#coding-standards)
- [Physics Guidelines](#physics-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

---

## How to Contribute

### Reporting Bugs

Check [existing issues](https://github.com/Nitr0xis/GravityEngine/issues) first. Include:

- Steps to reproduce
- Expected vs. actual behavior
- OS, Python version, Pygame version
- Running from source or executable
- Relevant log excerpt from `user_data/logs/gravityengine.log` if available

### Suggesting Enhancements

Check [ROADMAP.md](ROADMAP.md) first. Include:

- The problem being solved
- Proposed solution
- Alternatives considered
- Physics/technical rationale if applicable

### Priority Areas

- Bug fixes, stability
- Performance (the N-body force loop is O(n²); anything sublinear-ish is welcome)
- Physics accuracy
- Save/load, scenario presets, data export (see roadmap)
- Tests

---

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/GravityEngine.git
cd GravityEngine
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate    # macOS/Linux
pip install pygame matplotlib
git checkout -b feature/your-feature-name
```

Edit code in `src/`, docs in `README.md` / `ROADMAP.md`, build scripts in `builders/`.

Test by running `python src/engine.py` and exercising the change manually (creation, fusion, pause/resume, vectors, random mode as relevant).

---

## Coding Standards

Follow [PEP 8](https://pep8.org/). Concretely:

```python
# Good
def calculate_gravitational_force(mass1: float, mass2: float, distance: float) -> float:
    """Gravitational force between two bodies (Newtons)."""
    G = 6.6743e-11
    if distance == 0:
        return 0
    return G * (mass1 * mass2) / (distance ** 2)

# Avoid
def calc_force(m1,m2,d):
    return 6.6743e-11*(m1*m2)/(d**2)
```

- Classes: `PascalCase`. Functions/variables: `snake_case`. Constants: `UPPER_SNAKE_CASE`. Private attributes: `_leading_underscore`.
- Every public function/method gets a docstring (Args/Returns, and Note for edge cases).
- Use type hints.
- Handle edge cases explicitly (zero mass, zero distance, division by zero) rather than letting them raise or silently misbehave.

---

## Physics Guidelines

- Use verified formulas — don't invent physics. `F = G·(m1·m2)/r²`, not approximations without justification.
- Conservation laws matter: momentum must be conserved in collisions; document when energy is intentionally not conserved (inelastic fusion).
- SI units throughout: kg, m, s, N, J.
- Document physics assumptions in the docstring (e.g. "perfectly inelastic, no energy loss, spherical uniform-density bodies").
- Guard against division by zero and cap extreme force values.

---

## Commit Guidelines

Format: `<type>: <subject>`, where type is one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `chore`.

```bash
git commit -m "feat: add QuadTree spatial partitioning"
git commit -m "fix: correct momentum conservation in fusion calculation"
git commit -m "perf: optimize force calculation loop by 40%"
```

Avoid vague messages ("fixed stuff", "wip"). For complex changes, add a body explaining what changed and why, and reference the issue (`Resolves #42`).

---

## Pull Request Process

Before submitting:

- Code follows PEP 8, functions have docstrings
- Physics verified (formulas, conservation laws)
- Manually tested
- No leftover debug `print()` calls
- Docs updated if the change is user-facing

PR description should cover: what changed, why, how it was tested, and physics verification if applicable.

Review: maintainer checks code quality, physics accuracy, and does manual testing before merge. Response time is typically a few days — this is a solo-maintained student project, not a company.

---

## Testing

Manual checklist:

- Program starts, bodies can be created, move, and attract each other
- Pause/resume, selection, deletion work
- Two-body orbit is stable; momentum conserved in collisions; fusion mass is correct
- No FPS drop with under 100 bodies, no memory leak on long runs
- Edge cases: zero-mass bodies, overlapping bodies at creation, extreme time acceleration

Automated tests live in `debugger.py` (`test_force_summation`, `test_determinism`, `test_position_interpolation`, etc.) — extend these when touching physics code.

---

## Contact

Email: [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com)
Issues: [github.com/Nitr0xis/GravityEngine/issues](https://github.com/Nitr0xis/GravityEngine/issues)

Core maintainer: Nils DONTOT ([@Nitr0xis](https://github.com/Nitr0xis))

*Last updated: July 2026 — v3.8.0*
