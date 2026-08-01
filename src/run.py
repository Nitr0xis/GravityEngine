import pygame

from core import state
from core.main import Engine
from core.logger import Logger


if __name__ == '__main__':
    """
    Main entry point for the Gravity Engine simulation.
    
    Initializes pygame, sets up color constants, creates the engine instance,
    and starts the simulation loop.
    """
    # Initialize pygame modules
    pygame.init()

    # Create and run the simulation engine
    state.engine = Engine()

    try:
        state.engine.run()
    except Exception as e:
        Logger.exception(f"Engine crashed in main loop: {e}")
        raise e
        