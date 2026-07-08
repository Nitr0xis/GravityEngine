import sys
import os
import time
import pygame
import state
from typing import Optional
from temp_text import TempText
from config_panel import ConfigPanel
from circle import Circle
from math import fabs, sqrt
from logger import Logger


class ActionManager:
    """
    Static class for handling user actions and input events.
    
    All methods are static as they operate on the global engine instance
    and don't require their own state.
    """
    @staticmethod
    def toggle_pause():
        """Toggle simulation pause state."""
        if state.engine.is_paused:
            state.engine.unpause()
        else:
            state.engine.pause()
        Logger.info(f"Simulation paused: {state.engine.is_paused}")

    @staticmethod
    def toggle_gravitational_grid():
        state.engine.gravitational_grid_enabled = not state.engine.gravitational_grid_enabled
        label = "activée" if state.engine.gravitational_grid_enabled else "désactivée"  # renommer
        TempText(
            f"Grille gravitationnelle {label}",
            1.5,
            (20, state.engine.screen.get_height() - 2 * (state.engine.txt_gap + state.engine.txt_size)),
        )
        Logger.info(f"Gravitational grid: {state.engine.gravitational_grid_enabled}")

    @staticmethod
    def toggle_random_mode():
        """Toggle random velocity mode for new bodies."""
        state.engine.random_mode = not state.engine.random_mode
        Logger.info(f"Random mode: {state.engine.random_mode}")

    @staticmethod
    def toggle_reversed_gravity():
        """Toggle reversed gravity mode (repulsion instead of attraction)."""
        state.engine.reversed_gravity = not state.engine.reversed_gravity
        Logger.info(f"Reversed gravity: {state.engine.reversed_gravity}")

    @staticmethod
    def toggle_vectors_printed():
        """Toggle display of velocity and force vectors."""
        state.engine.vectors_printed = not state.engine.vectors_printed
        Logger.info(f"Vectors printed: {state.engine.vectors_printed}")

    @staticmethod
    def quit_engine(text: Optional[str] = None):
        """
        Quit the simulation and exit the program.
        
        Args:
            text: Exit message (not currently displayed)
        """
        if text is None:
            text = f"{60 * "="}\nSee you soon! Project available on https://github.com/Nitr0xis/GravityEngine/\n{60 * "="}"

        Logger.info("Quitting engine")
        pygame.quit()
        sys.exit(text)

    @staticmethod
    def delete_selected_circle():
        """Delete the currently selected body from the simulation."""
        for circle in state.circles:
            if circle.is_selected:
                state.circles.remove(circle)
                break
        Logger.info(f"Deleted selected circle : ID={circle.number}")

    @staticmethod
    def handle_mouse_button_down(event: pygame.event):
        """Handle mouse button press with camera transformation."""
        # Don't handle circle creation if in info mode
        if state.engine.show_help:
            return

        # Don't handle circle creation if config panel is open
        if state.engine.config_panel is not None and state.engine.config_panel.visible:
            return

        # Right click to pan
        if event.button == 3:  # Right click
            mx, my = pygame.mouse.get_pos()
            state.engine.camera.start_pan(mx, my)
            return

        # Left click for selection/creation
        if event.button == 1:  # Left click
            state.engine.circle_collided = None
            state.engine.can_create_circle = False
            state.engine.mouse_down = True
            state.engine.mouse_down_start_time = time.time()
            
            # Convert screen position to world coordinates
            screen_x, screen_y = pygame.mouse.get_pos()
            world_x, world_y = state.engine.camera.screen_to_world(screen_x, screen_y)
            
            if len(state.circles) > 0:
                alpha = state.engine.current_alpha

                # Check collision with bodies (visual positions)
                for circle in state.circles:
                    # Interpolated visual position (world)
                    visual_world_x = circle.prev_x + (circle.x - circle.prev_x) * alpha
                    visual_world_y = circle.prev_y + (circle.y - circle.prev_y) * alpha

                    # Distance in world coordinates
                    dx = fabs(world_x - visual_world_x)
                    dy = fabs(world_y - visual_world_y)
                    dist = sqrt(dx**2 + dy**2)

                    # Check if click is within the radius
                    if dist <= circle.radius:
                        state.engine.circle_collided = circle.number
                        for c in state.circles:
                            if c != circle:
                                c.is_selected = False
                        break

                # Selection handling
                if state.engine.circle_collided is not None:
                    for circle in state.circles:
                        if circle.number == state.engine.circle_collided:
                            circle.switch_selection()
                            break
                elif state.engine.circle_selected:
                    for circle in state.circles:
                        circle.is_selected = False
                else:
                    state.engine.can_create_circle = True

                if state.engine.can_create_circle:
                    # Create in world coordinates
                    state.engine.temp_circle = Circle(world_x, world_y, 
                                            state.engine.default_density, 
                                            mass=state.engine.minimum_mass)
                    state.engine.can_create_circle = False
            else:
                # Create in world coordinates
                state.engine.temp_circle = Circle(world_x, world_y, 
                                        state.engine.default_density, 
                                        mass=state.engine.minimum_mass)

        # Handle mouse wheel for zoom.
        if event.button == 4:  # Scroll up
            state.engine.camera.zoom_at_mouse(zoom_in=True)
        elif event.button == 5:  # Scroll down
            state.engine.camera.zoom_at_mouse(zoom_in=False)

    @staticmethod
    def handle_mouse_button_up(event: pygame.event):
        """
        Handle mouse button release events.
        
        Finalizes body creation by adding the temporary body to the simulation.
        
        Args:
            event: Pygame mouse button event
        """
        # Don't handle circle creation if in info mode
        if state.engine.show_help:
            return

        # End pan handling
        if event.button == 3:  # Right click
            state.engine.camera.end_pan()
            return
        
        # End of body creation
        if event.button == 1:  # Left click
            state.engine.mouse_down = False
            state.engine.mouse_down_start_time = None
            if state.engine.temp_circle is not None:
                state.circles.append(state.engine.temp_circle)
                state.engine.temp_circle = None

    @staticmethod
    def zoom_in():
        """Zoom in centered on screen center."""
        screen_center_x = state.engine.screen.get_width() // 2
        screen_center_y = state.engine.screen.get_height() // 2
        
        # Save mouse position
        old_mouse_pos = pygame.mouse.get_pos()
        
        # Simulate mouse in the middle
        pygame.mouse.set_pos(screen_center_x, screen_center_y)
        state.engine.camera.zoom_at_mouse(zoom_in=True)
        
        # Reload mouse position
        pygame.mouse.set_pos(old_mouse_pos)

    @staticmethod
    def zoom_out():
        """Zoom out centered on screen center."""
        screen_center_x = state.engine.screen.get_width() // 2
        screen_center_y = state.engine.screen.get_height() // 2
        
        old_mouse_pos = pygame.mouse.get_pos()
        pygame.mouse.set_pos(screen_center_x, screen_center_y)
        state.engine.camera.zoom_at_mouse(zoom_in=False)
        pygame.mouse.set_pos(old_mouse_pos)

    @staticmethod
    def reset_camera():
        """Reset camera to default position and zoom."""
        state.engine.camera.reset()
        TempText("Camera reset",
                1.5,
                (int((state.engine.screen.get_width() / 2) - (state.engine.font.size("Camera reset")[0] / 2)),
                state.engine.info_y - state.engine.txt_gap - state.engine.txt_size),
                line=1
                )
        Logger.info("Camera reset")

    @staticmethod
    def pan_camera(dx, dy):
        """Pan camera by offset."""
        state.engine.camera.cam_x += dx
        state.engine.camera.cam_y += dy

    @staticmethod
    def save_screenshot(path: Optional[str] = None):
        """
        Save a screenshot of the current screen.

        Args:
            path (Optional[str]): file path ending with .png
        """
        from logger import Logger
        
        surf = state.engine.screen.copy()
        state.engine.last_screenshot_surface = surf
        state.engine.fm.create_folder("screenshots")
        if path is None:
            file_name = f"screenshot_{int(time.time())}.png"
            full_path = os.path.join(state.engine.screenshots_folder_path, file_name)
        else:
            full_path = path
        try:
            pygame.image.save(surf, full_path)
            shown = os.path.basename(full_path)
            TempText(
                text=f"Screenshot enregistré : {shown}",
                duration=3.0,
                dest=(
                    20,
                    state.engine.screen.get_height() - 2 * (state.engine.txt_gap + state.engine.txt_size),
                ),
            )
            Logger.info(f"Screenshot saved: {shown}")
        except (pygame.error, OSError, ValueError, TypeError) as e:
            TempText(
                text=f"Échec capture : {e}",
                duration=3.0,
                dest=(
                    20,
                    state.engine.screen.get_height() - 2 * (state.engine.txt_gap + state.engine.txt_size),
                ),
            )
            Logger.exception(f"Screenshot failed: {e}")

    @staticmethod
    def open_config_panel():
        """Open/close the configuration panel."""
        if not hasattr(state.engine, 'config_panel') or state.engine.config_panel is None:
            state.engine.config_panel = ConfigPanel(state.engine, state.engine.screen, state.engine.used_font)
        
        state.engine.config_panel.toggle()
