# GravityEngine — N-body gravitational simulator
# Copyright (C) 2026 Nils DONTOT
# Contact: nils.dontot.pro@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import importlib.util
import subprocess
import sys
import warnings


def _ensure_dependencies(required: list[str] = None):
    """Checks and installs missing dependencies before launching."""
    if required is None:
        required = ["pygame", "numpy", "matplotlib"]

    missing = [pkg for pkg in required if importlib.util.find_spec(pkg) is None]

    if not missing:
        return

    print(f"Installing missing dependencies: {', '.join(missing)}")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
        importlib.invalidate_caches()
    except subprocess.CalledProcessError:
        warnings.warn(
            f"Automatic installation failed. Install manually with: "
            f"{sys.executable} -m pip install {' '.join(missing)}",
            stacklevel=1,
        )
        return

    # Vérification finale après installation
    still_missing = [pkg for pkg in missing if importlib.util.find_spec(pkg) is None]
    if still_missing:
        warnings.warn(
            f"Modules still missing after install attempt: {', '.join(still_missing)}. "
            f"Install manually with: {sys.executable} -m pip install {' '.join(still_missing)}",
            stacklevel=1,
        )


if __name__ == '__main__':
    """
    Main entry point for the Gravity Engine simulation.
    
    Initializes pygame, sets up color constants, creates the engine instance,
    and starts the simulation loop.
    """
    REQUIRED_DEPENDENCIES: list[str] = ["pygame", "numpy"]
    if not hasattr(sys, '_MEIPASS'):
        _ensure_dependencies(REQUIRED_DEPENDENCIES)

    import pygame
    from core import state
    from core.main import Engine
    from core.logger import Logger

    pygame.init()
    state.engine = Engine()

    try:
        state.engine.run()
    except Exception as e:
        Logger.exception(f"Engine crashed in main loop: {e}")
        raise e


# TODO list:
#   - Patch interpolation (BH?)
#   - Patch lens grid
        