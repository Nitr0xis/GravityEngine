import pygame


class Camera:
    def __init__(self, x: float = 0.0, y: float = 0.0, scale: float = 1.0, scale_step: float = 1.1):
        # ===== CAMERA POSITION =====
        self.cam_x = x  # Camera X offset (in screen pixels)
        self.cam_y = y  # Camera Y offset (in screen pixels)
        
        # ===== ZOOM =====
        self.scale = scale  # Zoom factor (1.0 = normal, 2.0 = 2x zoom)
        self.scale_step = scale_step  # Zoom multiplier (1.1 = +10% per step)
        
        # ===== LIMITS =====
        self.min_scale = 1e-7  # Minimum zoom (very zoomed out)
        self.max_scale = 100.0  # Maximum zoom (very zoomed in)
        
        # ===== PANNING =====
        self.pan_speed = 5.0  # Panning speed (pixels per frame)
        self.is_panning = False  # Whether we are currently panning the view
        self.pan_start_x = 0  # Pan start position X
        self.pan_start_y = 0

    def zoom_at_mouse(self, zoom_in: bool):
        """
        Zoom centered on the mouse position.
        
        Args:
            zoom_in: True to zoom in, False to zoom out
        """
        mx, my = pygame.mouse.get_pos()

        # World position BEFORE zoom
        wx, wy = self.screen_to_world(mx, my)

        # Apply zoom
        if zoom_in:
            self.scale *= self.scale_step
        else:
            self.scale /= self.scale_step

        # Clamp to allowed range
        self.scale = max(self.min_scale, min(self.scale, self.max_scale))

        # Recalculate offset to keep (wx, wy) under the mouse
        self.cam_x = mx - wx * self.scale
        self.cam_y = my - wy * self.scale
    
    def screen_to_world(self, sx, sy):
        """
        Convert screen coordinates → world coordinates.
        
        Args:
            sx, sy: Screen coordinates (pixels)
        
        Returns:
            wx, wy: World coordinates (meters)
        """
        wx = (sx - self.cam_x) / self.scale
        wy = (sy - self.cam_y) / self.scale
        return wx, wy

    def world_to_screen(self, wx, wy):
        """
        Convert world coordinates → screen coordinates.
        
        Args:
            wx, wy: World coordinates (meters)
        
        Returns:
            sx, sy: Screen coordinates (pixels)
        """
        sx = wx * self.scale + self.cam_x
        sy = wy * self.scale + self.cam_y
        return sx, sy
    
    def start_pan(self, mouse_x, mouse_y):
        """Start panning the view."""
        self.is_panning = True
        self.pan_start_x = mouse_x
        self.pan_start_y = mouse_y
    
    def update_pan(self, mouse_x, mouse_y):
        """Update the panning of the view."""
        if self.is_panning:
            # Calculate the mouse movement
            dx = mouse_x - self.pan_start_x
            dy = mouse_y - self.pan_start_y
            
            # Move the camera
            self.cam_x += dx
            self.cam_y += dy
            
            # Update the starting position
            self.pan_start_x = mouse_x
            self.pan_start_y = mouse_y
    
    def end_pan(self):
        """End view panning."""
        self.is_panning = False
    
    def reset(self):
        """Reset the camera to the default position."""
        self.cam_x = 0
        self.cam_y = 0
        self.scale = 1.0
