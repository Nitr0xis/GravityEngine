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
        self.min_scale = 1e-8  # Minimum zoom (very zoomed out)
        self.max_scale = 100.0  # Maximum zoom (very zoomed in)
        
        # ===== PANNING =====
        self.pan_speed = 5.0  # Panning speed (pixels per frame)
        self.is_panning = False  # Whether we are currently panning the view
        self.pan_start_x = 0  # Pan start position X
        self.pan_start_y = 0

        # Visual reference-frame origin (world meters / m/s). Physics coords are unchanged;
        # rendering and picking are expressed relative to this origin.
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.origin_vx = 0.0
        self.origin_vy = 0.0

    def zoom_at_mouse(self, zoom_in: bool):
        """
        Zoom centered on the mouse position.
        
        Args:
            zoom_in: True to zoom in, False to zoom out
        """
        mx, my = pygame.mouse.get_pos()
        self.zoom_anchored(zoom_in, (mx, my))

    def screen_to_view(self, sx, sy):
        """Screen pixels → coordinates relative to the visual frame origin."""
        return (sx - self.cam_x) / self.scale, (sy - self.cam_y) / self.scale

    def view_to_screen(self, vx, vy):
        """Visual-frame coordinates → screen pixels."""
        return vx * self.scale + self.cam_x, vy * self.scale + self.cam_y

    def screen_to_world(self, sx, sy):
        """
        Convert screen coordinates → world coordinates.
        
        Args:
            sx, sy: Screen coordinates (pixels)
        
        Returns:
            wx, wy: World coordinates (meters)
        """
        vx, vy = self.screen_to_view(sx, sy)
        return vx + self.origin_x, vy + self.origin_y

    def world_to_screen(self, wx, wy):
        """
        Convert world coordinates → screen coordinates.
        
        Args:
            wx, wy: World coordinates (meters)
        
        Returns:
            sx, sy: Screen coordinates (pixels)
        """
        return self.view_to_screen(wx - self.origin_x, wy - self.origin_y)

    def set_view_origin(self, ox: float, oy: float, ovx: float = 0.0, ovy: float = 0.0) -> None:
        """Set the visual frame origin without moving bodies."""
        self.origin_x = ox
        self.origin_y = oy
        self.origin_vx = ovx
        self.origin_vy = ovy

    def clear_view_origin(self) -> None:
        """Return picking/rendering to the world frame, keeping the current view."""
        self.cam_x -= self.origin_x * self.scale
        self.cam_y -= self.origin_y * self.scale
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.origin_vx = 0.0
        self.origin_vy = 0.0
    
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
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.origin_vx = 0.0
        self.origin_vy = 0.0

    def center_on(self, wx: float, wy: float, screen_w: int, screen_h: int):
        """Recenter the camera so that world point (wx, wy) is at the screen center."""
        self.cam_x = screen_w / 2 - (wx - self.origin_x) * self.scale
        self.cam_y = screen_h / 2 - (wy - self.origin_y) * self.scale

    def zoom_anchored(self, zoom_in: bool, anchor_screen_pos: tuple[float, float]):
        """
        Zoom while keeping a given screen point fixed in the visual frame.
        Generalizes zoom_at_mouse: the anchor can be the mouse (normal behavior) or the screen center (focus mode).
        """
        ax, ay = anchor_screen_pos
        vx, vy = self.screen_to_view(ax, ay)

        if zoom_in:
            self.scale *= self.scale_step
        else:
            self.scale /= self.scale_step
        self.scale = max(self.min_scale, min(self.scale, self.max_scale))

        self.cam_x = ax - vx * self.scale
        self.cam_y = ay - vy * self.scale
