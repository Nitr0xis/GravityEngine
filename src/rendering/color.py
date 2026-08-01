class Color:
    def __init__(self, *values):
        if len(values) not in (3, 4):
            raise ValueError("Color must have 3 (RGB) or 4 (RGBA) values")
        
        if not all(isinstance(v, int) and 0 <= v <= 255 for v in values):
            raise ValueError("All values must be integers between 0 and 255")
        
        self._value = tuple[int, ...](values)
    
    @property
    def value(self):
        return self._value
    
    @property
    def rgb(self):
        return self._value[:3]
    
    @property
    def alpha(self):
        return self._value[3] if len(self._value) == 4 else 255
    
    @property
    def average(self):
        """Returns the mean of the RGB components (average brightness)"""
        return sum(self.rgb) / 3
    
    @property
    def luminosity(self):
        """Perceived luminosity (standard formula for comparisons)"""
        r, g, b = self.rgb
        return 0.299 * r + 0.587 * g + 0.114 * b
    
    def __iter__(self):
        """Allows: tuple(color), list(color), *color"""
        return iter(self._value)

    def __getitem__(self, index):
        """Allows: color[0], color[1], color[2]"""
        return self._value[index]

    def __len__(self):
        """Allows: len(color)"""
        return len(self._value)
    
    # ADDITION: color1 + color2
    def __add__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only add another Color")
        
        max_len = max(len(self._value), len(other._value))
        v1 = self._value + (255,) * (max_len - len(self._value))
        v2 = other._value + (255,) * (max_len - len(other._value))
        
        result = tuple(min(255, a + b) for a, b in zip(v1, v2))
        return Color(*result)
    
    # SUBTRACTION: color1 - color2
    def __sub__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only subtract another Color")
        
        max_len = max(len(self._value), len(other._value))
        v1 = self._value + (255,) * (max_len - len(self._value))
        v2 = other._value + (255,) * (max_len - len(other._value))
        
        result = tuple(max(0, a - b) for a, b in zip(v1, v2))
        return Color(*result)
    
    # MULTIPLICATION: color * 2 or color * 0.5
    def __mul__(self, factor):
        if not isinstance(factor, (int, float)):
            raise TypeError("Can only multiply by a number")
        
        result = tuple(int(min(255, max(0, v * factor))) for v in self._value)
        return Color(*result)
    
    def __rmul__(self, factor):
        return self.__mul__(factor)
    
    # DIVISION: color / 2
    def __truediv__(self, factor):
        if not isinstance(factor, (int, float)):
            raise TypeError("Can only divide by a number")
        if factor == 0:
            raise ValueError("Division by zero")
        
        result = tuple(int(min(255, max(0, v / factor))) for v in self._value)
        return Color(*result)
    
    # AVERAGE: color1 // color2
    def __floordiv__(self, other):
        if not isinstance(other, Color):
            raise TypeError("Can only average with another Color")
        
        max_len = max(len(self._value), len(other._value))
        v1 = self._value + (255,) * (max_len - len(self._value))
        v2 = other._value + (255,) * (max_len - len(other._value))
        
        result = tuple((a + b) // 2 for a, b in zip(v1, v2))
        return Color(*result)
    
    # EQUALITY: color1 == color2
    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return self._value == other._value
    
    # DIFFERENCE: color1 != color2
    def __ne__(self, other):
        return not self.__eq__(other)
    
    # COMPARISONS (based on perceived luminosity)
    def __lt__(self, other):
        """color1 < color2: compares luminosity"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity < other.luminosity
    
    def __le__(self, other):
        """color1 <= color2"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity <= other.luminosity
    
    def __gt__(self, other):
        """color1 > color2"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity > other.luminosity
    
    def __ge__(self, other):
        """color1 >= color2"""
        if not isinstance(other, Color):
            raise TypeError("Can only compare with another Color")
        return self.luminosity >= other.luminosity
    
    def __repr__(self):
        return f"Color{self._value}"
    
    def __str__(self):
        r, g, b = self.rgb
        if len(self._value) == 4:
            return f"Color(R:{r}, G:{g}, B:{b}, A:{self.alpha})"
        return f"Color(R:{r}, G:{g}, B:{b})"


class Display:
    # Color constants (RGB tuples)
    # These define the color palette used throughout the simulation
    WHITE = Color(255, 255, 255)  # Default body color in dark mode
    BLUE = Color(10, 124, 235)  # UI text and information color
    SP_BLUE = Color(130, 130, 220)  # Special blue for force vectors
    BLACK = Color(0, 0, 0)  # Background in dark mode, default body color in light mode
    DUCKY_GREEN = Color(28, 201, 89)  # Selection highlight color
    GREEN = Color(0, 255, 0)  # X-component velocity vector color
    YELLOW = Color(241, 247, 0)  # Y-component velocity vector color
    DARK_GREY = Color(100, 100, 100)  # Body shadow/outline color
    RED = Color(255, 0, 0)  # Global velocity vector color
    