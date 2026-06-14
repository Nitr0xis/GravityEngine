import time
import state
from utils import Utils


class TempText:
    """
    Temporary text display class for showing messages on screen.
    
    Automatically manages its own lifecycle - removes itself from the display
    list when the duration expires. Used for notifications and status messages.
    """
    def __init__(self, text: str = "", duration: float = 1, dest: tuple[float, float] = (0, 0), line: int = 0,
                 color: tuple[int, int, int] | tuple[int, int, int, int] = (10, 124, 235)):
        """
        Initialize a temporary text object.
        
        Args:
            text: The text string to display
            duration: How long the text should remain visible (in seconds)
            dest: Initial position (x, y) on screen
            line: Line offset for vertical spacing (0 = first line)
            color: RGB or RGBA color tuple for the text
        """
        super().__init__()

        # Register this text in the engine's temporary texts list
        state.engine.temp_texts.append(self)

        # Record creation time for expiration checking
        self.birth_time = time.time()

        # Store text properties
        self.text = text
        self.duration = duration

        # Calculate position with line offset
        self.x = dest[0]
        self.y = dest[1] + line * (state.engine.txt_gap + state.engine.txt_size)
        self.line = line
        self.color = color

        # Rectangle for collision/position tracking (not currently used)
        self.rect = None

    def update(self):
        """
        Update the temporary text - draw it if still valid, remove if expired.
        
        Returns:
            True if text is still active, False if expired and removed
        """
        # Check if duration has expired
        if time.time() - self.birth_time > self.duration:
            # Remove from list if still present
            if self in state.engine.temp_texts:
                state.engine.temp_texts.remove(self)
            return False
        else:
            # Draw the text at its position
            Utils.write_screen(self.text, (self.x, self.y), self.color)
            return True
