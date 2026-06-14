import state
import pygame
from typing import Optional
from color import Color, Display


class Utils:
    """
    Utility class providing helper functions for calculations and rendering.
    
    All methods are static utility functions that don't require instance state.
    """
    @staticmethod
    def heaviest() -> Optional[tuple]:
        """
        Find the heaviest body in the simulation.
        
        Returns:
            Tuple of (body_id, mass) if bodies exist, None otherwise
        """
        circles_mass = []

        if len(state.circles) != 0:
            # Collect all body masses
            for circle in state.circles:
                circles_mass.append(circle.mass)

            # Find index of maximum mass
            index = circles_mass.index(max(circles_mass))
            circle_id = state.circles[index].number

            return circle_id, max(circles_mass)
        else:
            return None

    @staticmethod
    def oldest() -> Optional[tuple]:
        """
        Find the oldest body in the simulation.
        
        Returns:
            Tuple of (body_id, age) if bodies exist, None otherwise
        """
        circles_age = []

        if len(state.circles) != 0:
            # Collect all body ages
            for circle in state.circles:
                circles_age.append(circle.age)

            # Find index of maximum age
            index = circles_age.index(max(circles_age))
            circle_id = state.circles[index].number

            return circle_id, max(circles_age)
        else:
            return None

    @staticmethod
    def mass_sum() -> float:
        """
        Calculate total mass of all bodies in the simulation.
        
        Returns:
            Sum of all body masses
        """
        total = 0.0
        for circle in state.circles:
            total += float(circle.mass)
        return total

    @staticmethod
    def draw_line(color: tuple[int, int, int] | tuple[int, int, int, int] = (255, 255, 255),
                  start_pos: tuple[float, float] = (0, 0),
                  end_pos: tuple[float, float] = (0, 0),
                  width: int = 1):
        """
        Draw a line on the screen.
        
        Args:
            color: RGB or RGBA color tuple
            start_pos: Starting position (x, y)
            end_pos: Ending position (x, y)
            width: Line width in pixels
        """
        pygame.draw.line(state.engine.screen, color, start_pos, end_pos, width)
    
    @staticmethod
    def write_screen(text: str = "[text]",
              dest: tuple[int, int] = (0, 0),
              color: tuple[int, int, int] = Color(255, 255, 255),
              line: int = 0) -> Optional[pygame.Rect]:
        """
        Render and display text on the screen.
        
        Args:
            text: Text string to display
            dest: Base position (x, y) for text
            color: RGB color tuple
            line: Line offset for vertical spacing (0 = first line)
        
        Returns:
            Pygame Rect object representing the text area, or None on error
        """
        written = state.engine.font.render(text, 1, color)
        rect = state.engine.screen.blit(written, dest=(dest[0], dest[1] + line * (state.engine.txt_gap + state.engine.txt_size)))
        return rect

    @staticmethod
    def average(l: list[float] | tuple[float] | set[float]) -> float:
        """
        Calculate arithmetic mean of a sequence of numbers.
        
        Args:
            l: Sequence of numbers (list, tuple, or set)
        
        Returns:
            Average value, or 0 if sequence is empty
        """
        return sum(l) / len(l) if len(l) > 0 else 0
