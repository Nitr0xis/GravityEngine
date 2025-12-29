"""
Gravity Engine by Nils DONTOT

Touches:
    - Espace -> faire pause/depause
    - Molette (facultatif) -> crée les plus petits cops possibles
    - V -> activer/desactiver les vecteurs de vitesse
    - R -> activer/desactiver le random_mode
    - G -> activer/desactiver la gravité inversé
    - Clique droit/gauche/molette -> maintenir pour faire apparaitre des corps
                                  -> selectionner/deselectionner un corps
    - Suppr -> Supprimer un corps selectionné
"""


# import ensurepip
import importlib.util
import random
import subprocess
import time
import math
import sys

from math import *

required_moduls: set[str] = {'pygame', 'numpy'}

# ensurepip.bootstrap()

for modul in required_moduls:
    if importlib.util.find_spec(modul) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", modul])

import pygame
import numpy as np

# Essayer d'importer CuPy pour GPU, sinon utiliser NumPy (CPU)
GPU_AVAILABLE = False
cp = None

try:
    import cupy as cp
    # Tester si le GPU est réellement utilisable
    try:
        # Test simple pour vérifier que le GPU fonctionne
        test_array = cp.zeros(1)
        del test_array
        GPU_AVAILABLE = True
        print("CuPy détecté - Utilisation du GPU")
    except Exception as e:
        # GPU non disponible (pilote CUDA insuffisant, pas de GPU, etc.)
        cp = np
        GPU_AVAILABLE = False
        print(f"CuPy détecté mais GPU non utilisable - Utilisation de NumPy (CPU)")
        print(f"Raison: {type(e).__name__}")
        if "CUDARuntimeError" in str(type(e)) or "cudaError" in str(e):
            print("Le pilote CUDA est insuffisant ou le GPU n'est pas accessible.")
            print("Mise à jour du pilote NVIDIA recommandée pour utiliser le GPU.")
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cupy-cuda12x"], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import cupy as cp
        # Tester si le GPU est réellement utilisable après installation
        try:
            test_array = cp.zeros(1)
            del test_array
            GPU_AVAILABLE = True
            print("CuPy installé - Utilisation du GPU")
        except Exception as e:
            cp = np
            GPU_AVAILABLE = False
            print(f"CuPy installé mais GPU non utilisable - Utilisation de NumPy (CPU)")
            print(f"Raison: {type(e).__name__}")
    except:
        cp = np
        GPU_AVAILABLE = False
        print("CuPy non disponible - Utilisation de NumPy (CPU)")
        print("Pour utiliser le GPU, installez CuPy: pip install cupy-cuda12x (ou cupy-cuda11x selon votre version CUDA)")

"""
Les parametre sont modulables des lignes 437 à 480.
Les commandes y sont indiquées.

To-do : 
    - corriger random_mode


### ajouter limite de roche

"""


def rac2(number) -> float:
    return number ** (1 / 2)


def rac3(number) -> float:
    if number == 0:
        return 0
    else:
        return abs(number) / number * abs(number) ** (1 / 3)


def cos(angle) -> float:
    return math.cos(angle)


def sin(angle) -> float:
    return math.sin(angle)


def atan2(y, x) -> float:  # return Radians
    return math.atan2(y, x)


def draw_line(color: tuple[int, int, int] | tuple[int, int, int, int] = (255, 255, 255),
              start_pos: tuple[float, float] = (0, 0), end_pos: tuple[float, float] = (0, 0), width: int = 1):
    pygame.draw.line(game.screen, color, start_pos, end_pos, width)


def moy(l: list[float] | tuple[float] | set[float]) -> float:
    return sum(l) / len(l)


# -----------------
# class GPUDataManager
# -----------------
class GPUDataManager:
    """Gère tous les arrays GPU pour les calculs vectorisés"""
    def __init__(self):
        # Utilise CuPy si disponible et fonctionnel, sinon NumPy
        if GPU_AVAILABLE and cp is not None:
            self.xp = cp
        else:
            self.xp = np
        self.max_circles = 10000  # Taille maximale initiale
        self.current_size = 0
        
        # Arrays GPU pour toutes les données
        self.positions_x = None
        self.positions_y = None
        self.velocities_x = None
        self.velocities_y = None
        self.masses = None
        self.radii = None
        self.basic_masses = None
        
        # Arrays pour les forces (temporaires)
        self.forces_x = None
        self.forces_y = None
        
        # Mapping: index dans l'array -> Circle object
        self.index_to_circle = {}
        self.circle_to_index = {}
        
    def initialize_arrays(self, size=None):
        """Initialise ou redimensionne les arrays GPU"""
        if size is None:
            size = self.max_circles
        else:
            self.max_circles = max(self.max_circles, size)
        
        dtype = self.xp.float32
        
        # Si on utilise CuPy et qu'il y a une erreur CUDA, basculer vers NumPy
        try:
            self.positions_x = self.xp.zeros(size, dtype=dtype)
            self.positions_y = self.xp.zeros(size, dtype=dtype)
            self.velocities_x = self.xp.zeros(size, dtype=dtype)
            self.velocities_y = self.xp.zeros(size, dtype=dtype)
            self.masses = self.xp.zeros(size, dtype=dtype)
            self.radii = self.xp.zeros(size, dtype=dtype)
            self.basic_masses = self.xp.zeros(size, dtype=dtype)
            self.forces_x = self.xp.zeros(size, dtype=dtype)
            self.forces_y = self.xp.zeros(size, dtype=dtype)
        except Exception as e:
            # Si erreur CUDA, basculer vers NumPy
            if "cuda" in str(e).lower() or "CUDARuntimeError" in str(type(e)):
                global GPU_AVAILABLE, cp
                print(f"\nErreur CUDA détectée lors de l'initialisation: {e}")
                print("Basculement automatique vers NumPy (CPU)...")
                self.xp = np
                cp = np
                GPU_AVAILABLE = False
                # Réessayer avec NumPy
                self.positions_x = self.xp.zeros(size, dtype=dtype)
                self.positions_y = self.xp.zeros(size, dtype=dtype)
                self.velocities_x = self.xp.zeros(size, dtype=dtype)
                self.velocities_y = self.xp.zeros(size, dtype=dtype)
                self.masses = self.xp.zeros(size, dtype=dtype)
                self.radii = self.xp.zeros(size, dtype=dtype)
                self.basic_masses = self.xp.zeros(size, dtype=dtype)
                self.forces_x = self.xp.zeros(size, dtype=dtype)
                self.forces_y = self.xp.zeros(size, dtype=dtype)
            else:
                raise  # Relancer l'erreur si ce n'est pas une erreur CUDA
        
    def add_circle(self, circle, index):
        """Ajoute un cercle aux arrays GPU"""
        if self.positions_x is None or index >= len(self.positions_x):
            new_size = max(self.max_circles, (index + 1) * 2)
            self.initialize_arrays(new_size)
        
        self.positions_x[index] = float(circle.x)
        self.positions_y[index] = float(circle.y)
        self.velocities_x[index] = float(circle.vx)
        self.velocities_y[index] = float(circle.vy)
        self.masses[index] = float(circle.mass)
        self.radii[index] = float(circle.radius)
        self.basic_masses[index] = float(circle.basic_mass)
        
        self.index_to_circle[index] = circle
        self.circle_to_index[circle] = index
        self.current_size = max(self.current_size, index + 1)
        
    def update_circle_from_gpu(self, circle):
        """Met à jour un cercle depuis les données GPU"""
        if circle in self.circle_to_index:
            idx = self.circle_to_index[circle]
            # Synchroniser depuis GPU vers CPU
            if GPU_AVAILABLE and self.xp is cp and hasattr(cp, 'asnumpy'):
                circle.x = float(cp.asnumpy(self.positions_x[idx]))
                circle.y = float(cp.asnumpy(self.positions_y[idx]))
                circle.vx = float(cp.asnumpy(self.velocities_x[idx]))
                circle.vy = float(cp.asnumpy(self.velocities_y[idx]))
                circle.mass = float(cp.asnumpy(self.masses[idx]))
                circle.radius = float(cp.asnumpy(self.radii[idx]))
            else:
                # NumPy ou CuPy non disponible - conversion directe
                circle.x = float(self.positions_x[idx])
                circle.y = float(self.positions_y[idx])
                circle.vx = float(self.velocities_x[idx])
                circle.vy = float(self.velocities_y[idx])
                circle.mass = float(self.masses[idx])
                circle.radius = float(self.radii[idx])
                
    def update_circle_to_gpu(self, circle):
        """Met à jour les arrays GPU depuis un cercle"""
        if circle in self.circle_to_index:
            idx = self.circle_to_index[circle]
            self.positions_x[idx] = float(circle.x)
            self.positions_y[idx] = float(circle.y)
            self.velocities_x[idx] = float(circle.vx)
            self.velocities_y[idx] = float(circle.vy)
            self.masses[idx] = float(circle.mass)
            self.radii[idx] = float(circle.radius)
            
    def remove_circle(self, circle):
        """Retire un cercle des arrays (marque comme supprimé)"""
        if circle in self.circle_to_index:
            idx = self.circle_to_index[circle]
            # Marquer comme supprimé en mettant la masse à 0
            self.masses[idx] = 0.0
            del self.index_to_circle[idx]
            del self.circle_to_index[circle]
            
    def compute_gravity_forces(self, gravity, reversed_gravity, dt):
        """Calcule toutes les forces gravitationnelles de manière vectorisée sur GPU"""
        n = self.current_size
        if n == 0:
            return
            
        # Réinitialiser les forces
        self.forces_x.fill(0.0)
        self.forces_y.fill(0.0)
        
        # Extraire les données actives (masse > 0)
        active_mask = self.masses[:n] > 0
        
        if not self.xp.any(active_mask):
            return
            
        # Positions et masses actives
        px = self.positions_x[:n][active_mask]
        py = self.positions_y[:n][active_mask]
        m = self.masses[:n][active_mask]
        r = self.radii[:n][active_mask]
        
        # Calcul vectorisé de toutes les paires
        # dx[i,j] = px[j] - px[i]
        dx = px[:, None] - px[None, :]
        dy = py[:, None] - py[None, :]
        
        # Distance au carré
        dist_sq = dx**2 + dy**2
        
        # Éviter la division par zéro et les collisions
        min_dist = (r[:, None] + r[None, :])
        dist_sq = self.xp.maximum(dist_sq, min_dist**2)
        dist = self.xp.sqrt(dist_sq)
        
        # Force gravitationnelle: F = G * m1 * m2 / r^2
        force_magnitude = gravity * (m[:, None] * m[None, :]) / dist_sq
        
        # Direction de la force
        fx = force_magnitude * (dx / dist)
        fy = force_magnitude * (dy / dist)
        
        if reversed_gravity:
            fx = -fx
            fy = -fy
        
        # Somme des forces sur chaque corps
        # Masquer la diagonale (force sur soi-même)
        mask = self.xp.eye(len(px), dtype=bool)
        fx = self.xp.where(mask, 0, fx)
        fy = self.xp.where(mask, 0, fy)
        
        total_fx = self.xp.sum(fx, axis=1)
        total_fy = self.xp.sum(fy, axis=1)
        
        # Mettre à jour les vitesses: v += F/m * dt
        active_indices = self.xp.where(active_mask)[0]
        dt_corrected = dt * 100 * (1.0 / game.frequency) if hasattr(game, 'frequency') and game.frequency > 0 else dt
        
        # Éviter la division par zéro
        m_safe = self.xp.maximum(m, 1e-10)
        self.velocities_x[active_indices] += (total_fx / m_safe) * dt_corrected
        self.velocities_y[active_indices] += (total_fy / m_safe) * dt_corrected
        
        # Mettre à jour les positions: x += v * dt
        self.positions_x[active_indices] += self.velocities_x[active_indices] * dt_corrected * game.speed
        self.positions_y[active_indices] += self.velocities_y[active_indices] * dt_corrected * game.speed
        
        # Stocker les forces pour l'affichage
        self.forces_x[active_indices] = total_fx
        self.forces_y[active_indices] = total_fy
        
    def check_collisions_and_fusions(self, circles_list):
        """Vérifie les collisions et effectue les fusions sur GPU"""
        n = self.current_size
        if n < 2:
            return
            
        active_mask = self.masses[:n] > 0
        if not self.xp.any(active_mask):
            return
            
        px = self.positions_x[:n][active_mask]
        py = self.positions_y[:n][active_mask]
        m = self.masses[:n][active_mask]
        r = self.radii[:n][active_mask]
        vx = self.velocities_x[:n][active_mask]
        vy = self.velocities_y[:n][active_mask]
        
        active_indices = self.xp.where(active_mask)[0]
        
        # Calcul des distances
        dx = px[:, None] - px[None, :]
        dy = py[:, None] - py[None, :]
        dist = self.xp.sqrt(dx**2 + dy**2)
        min_dist = r[:, None] + r[None, :]
        
        # Masquer la diagonale
        mask = self.xp.eye(len(px), dtype=bool)
        collision_mask = (dist <= min_dist) & ~mask
        
        # Traiter les collisions (fusion)
        if self.xp.any(collision_mask):
            # Convertir en indices CPU pour traitement
            if GPU_AVAILABLE and self.xp is cp and hasattr(cp, 'asnumpy'):
                collision_mask_cpu = cp.asnumpy(collision_mask)
                active_indices_cpu = cp.asnumpy(active_indices)
            else:
                # NumPy ou CuPy non disponible - conversion directe
                collision_mask_cpu = collision_mask
                active_indices_cpu = active_indices
                
            # Traiter chaque collision
            for i in range(len(active_indices_cpu)):
                for j in range(i+1, len(active_indices_cpu)):
                    if collision_mask_cpu[i, j]:
                        idx_i = int(active_indices_cpu[i])
                        idx_j = int(active_indices_cpu[j])
                        
                        if idx_i in self.index_to_circle and idx_j in self.index_to_circle:
                            circle_i = self.index_to_circle[idx_i]
                            circle_j = self.index_to_circle[idx_j]
                            
                            if circle_i.mass >= circle_j.mass:
                                # Fusion: i absorbe j
                                total_mass = circle_i.mass + circle_j.mass
                                new_x = (circle_i.x * circle_i.mass + circle_j.x * circle_j.mass) / total_mass
                                new_y = (circle_i.y * circle_i.mass + circle_j.y * circle_j.mass) / total_mass
                                new_vx = (circle_i.vx * circle_i.mass + circle_j.vx * circle_j.mass) / total_mass
                                new_vy = (circle_i.vy * circle_i.mass + circle_j.vy * circle_j.mass) / total_mass
                                
                                self.positions_x[idx_i] = new_x
                                self.positions_y[idx_i] = new_y
                                self.velocities_x[idx_i] = new_vx
                                self.velocities_y[idx_i] = new_vy
                                self.masses[idx_i] = total_mass
                                
                                # Calculer le rayon avec rac3
                                if total_mass != 0:
                                    new_radius = abs(total_mass) / abs(total_mass) * abs(total_mass) ** (1/3)
                                else:
                                    new_radius = 0.0
                                
                                self.radii[idx_i] = new_radius
                                
                                # Mettre à jour l'objet circle_i
                                circle_i.x = float(new_x)
                                circle_i.y = float(new_y)
                                circle_i.vx = float(new_vx)
                                circle_i.vy = float(new_vy)
                                circle_i.mass = total_mass
                                circle_i.radius = float(new_radius)
                                
                                # Marquer j comme supprimé
                                circle_j.suicide = True
                                self.masses[idx_j] = 0.0


# -----------------
# class Camera
# -----------------
class Camera:
    def __init__(self, zoom_speed, moving_speed):
        super().__init__()

        self.zoom = 1
        self.pos: list[float] = [0, 0]

        self.zoom_speed = zoom_speed
        self.moving_speed = moving_speed

    def update_data(self):
        if pygame.K_a in game.inputs:
            self.zoom -= self.zoom_speed

        if pygame.K_e in game.inputs:
            self.zoom += self.zoom_speed

        # arrows
        if pygame.K_LEFT in game.inputs:
            self.pos[0] -= self.moving_speed

        if pygame.K_RIGHT in game.inputs:
            self.pos[0] += self.moving_speed

        if pygame.K_UP in game.inputs:
            self.pos[1] -= self.moving_speed

        if pygame.K_DOWN in game.inputs:
            self.pos[1] += self.moving_speed

    def update_visual(self):
        self.update_data()


# -----------------
# class Text
# -----------------
class Text:
    def __init__(self, text: str = "", duration: float = 1, dest: tuple[float, float] = (0, 0), line: int = 0,
                 color: tuple[int, int, int] | tuple[int, int, int, int] = (10, 124, 235)):
        super().__init__()

        game.texts.append(self)

        self.birthday = time.time()

        self.text = text
        self.duration = duration

        self.x = dest[0]
        self.y = dest[1] + line * (game.txt_gap + game.txt_size)
        self.line = line

        self.color = color

        self.rect = None

    def update(self):
        written = game.font.render(self.text, 1, self.color)
        self.rect = game.screen.blit(written, dest=(self.x, self.y + self.line * (game.txt_gap + game.txt_size)))
        return self.rect


# -----------------
# class Circle
# -----------------
class Circle:
    def __init__(self, x, y, radius, mass):
        super().__init__()

        self.pos = None
        self.full_selected_mode = False

        game.circle_number += 1
        self.number: int = game.circle_number

        self.x: float = float(x) if x is not None else 0.0
        self.y: float = float(y) if y is not None else 0.0

        self.basic_mass = mass
        self.mass = self.basic_mass

        self.radius = radius
        self.radiusn = self.mass ** (1 / 3)

        self.surface = 4 * self.radius ** 2 * math.pi
        self.volume = 4 / 3 * math.pi * self.radius ** 3

        self.rect = None

        if game.screen_mode == "dark":
            self.color = WHITE
        elif game.screen_mode == "light":
            self.color = BLACK

        self.is_selected = False
        if not self in circles:
            self.is_selected = False

        self.vx = 0
        self.vy = 0

        self.speed = rac2(self.vx ** 2 + self.vy ** 2) * game.FPS

        self.suicide: bool = False

        self.is_born = False
        self.birthday = None
        self.age = 0
        self.time_in_pause = 0

        self.info_y: int = 6 * game.txt_gap + 4 * game.txt_size

        self.vector_width = 1
        self.vector_length = game.vector_length

        self.GSV_color = RED
        self.CSVx_color = GREEN
        self.CSVy_color = YELLOW

        self.attract_forces: list[tuple[float, float]] = []
        self.force: list[float] = [0.0, 0.0]   # tjrs que deux elements
        self.printed_force: list[float] = [0.0, 0.0]    # tjrs que deux elements

    def draw(self, screen):
        # --- SECURITY ---
        if not isinstance(self.x, (int, float)):
            # Si c'est une liste/tuple, prendre le premier élément
            if isinstance(self.x, (list, tuple)) and len(self.x) > 0:
                self.x = float(self.x[0])
            else:
                # Sinon, réinitialiser à 0
                self.x = 0.0
                print(f"WARNING: Circle {self.number} had invalid x coordinate, reset to 0")

        if not isinstance(self.y, (int, float)):
            # Si c'est une liste/tuple, prendre le premier élément
            if isinstance(self.y, (list, tuple)) and len(self.y) > 0:
                self.y = float(self.y[0])
            else:
                # Sinon, réinitialiser à 0
                self.y = 0.0
                print(f"WARNING: Circle {self.number} had invalid y coordinate, reset to 0")

        if not isinstance(self.radius, (int, float)):
            # Si c'est une liste/tuple, prendre le premier élément
            if isinstance(self.radius, (list, tuple)) and len(self.radius) > 0:
                self.radius = float(self.radius[0])
            else:
                # Sinon, utiliser une valeur par défaut
                self.radius = 1.0
                print(f"WARNING: Circle {self.number} had invalid radius, reset to 1")
        # ----------------

        if self.full_selected_mode:
            if self.is_selected:
                self.color = DUCKY_GREEN
            else:
                if game.screen_mode == "dark":
                    self.color = WHITE
                elif game.screen_mode == "light":
                    self.color = BLACK
        else:
            if self.is_selected:
                if self.radius <= 4:
                    pygame.draw.circle(screen, DUCKY_GREEN, (int(self.x), int(self.y)), int(self.radius) + 1 + 1)
                elif self.radius <= 20:
                    pygame.draw.circle(screen, DUCKY_GREEN, (int(self.x), int(self.y)),
                                       int(self.radius) + self.radius / 4 + 1)
                else:
                    pygame.draw.circle(screen, DUCKY_GREEN, (int(self.x), int(self.y)), int(self.radius) + 4 + 1)

        if not self.is_selected:
            if self.radius <= 4:
                pygame.draw.circle(screen, DARK_GREY, (int(self.x), int(self.y)), int(self.radius) + 1)
            elif self.radius <= 20:
                pygame.draw.circle(screen, DARK_GREY, (int(self.x), int(self.y)), int(self.radius) + self.radius / 5)
            else:
                pygame.draw.circle(screen, DARK_GREY, (int(self.x), int(self.y)), int(self.radius) + 3)

        self.rect = pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

        """
        Debug tool:

        txt = game.font.render(f"{self.number}", 1, BLUE)    <- pour afficher les numero sur les cercles
        game.screen.blit(txt, (int(self.x), int(self.y)))
        """

    def speed_power(self):
        return 0.5 * self.mass * (self.speed ** 2)

    def switch_selection(self):
        if self.is_selected:
            self.is_selected = False
        else:
            self.is_selected = True

    def get_nearest(self) -> tuple[int, float] | None:
        """

        :return: (ID of the nearest, distance)
        """
        numbers = []
        distances = []

        for other in circles:

            if other is not self:
                numbers.append(other.number)
                distances.append(rac2((self.y - other.y) ** 2 + (self.x - other.x) ** 2))

        if len(distances) != 0:
            return numbers[distances.index(min(distances))], min(distances)

        else:
            return None

    def print_GSV(self, in_terminal: bool = False):
        x1 = self.x
        y1 = self.y

        x2 = self.vector_length * (self.x + self.vx * 17.5 * game.speed)
        y2 = self.vector_length * (self.y + self.vy * 17.5 * game.speed)

        if in_terminal:
            print(f"N{self.number} Start : ({x1}; {y1}); End : ({x2}; {y2})")

        draw_line(self.GSV_color, (x1, y1), (x2, y2), self.vector_width)
        if game.cardinals_vectors:
            self.print_CSV()

    def PrintStrengthV(self, in_terminal: bool = False):
        # self.force = (fx, fy)
        force = math.sqrt(self.force[0] ** 2 + self.force[1] ** 2)
        if force != 0:
            coefficient = 5 / force * rac3(force)
        else:
            coefficient = 0

        vector_x = self.force[0] * coefficient * game.vector_length * (math.sqrt(game.speed) / 8)
        vector_y = self.force[1] * coefficient * game.vector_length * (math.sqrt(game.speed) / 8)
        end_coordinates = (self.x + vector_x, self.y + vector_y)
        if in_terminal:
            print(f"N{self.number} Start : ({self.x}; {self.y}); End : {end_coordinates}")
        draw_line(SP_BLUE, (self.x, self.y), end_coordinates)

    def print_CSV(self, in_terminal: bool = False):
        x1 = self.x
        x2 = self.x + self.vx * 7

        y1 = self.y
        y2 = self.y + self.vy * 7

        if in_terminal:
            print(
                f"N{self.number} Start x : ({x1}; {self.y}); End x : ({x2}; {self.y}) Start y : ({y1}; {self.x}); End y : ({y2}; {self.x})")

        draw_line(self.CSVx_color, (x1, self.y), (x2, self.y), self.vector_width)
        draw_line(self.CSVy_color, (self.x, y1), (self.x, y2), self.vector_width)

    def print_info(self, y: int):
        pygame.draw.rect(game.screen, BLUE, (20, y, 340, 5))

        text = f"ID : {self.number}"
        game.write(text, (20, y - 20), BLUE, 1)

        if self.age * game.speed  / 31_557_600 < 2:
            text = f"Age : {round(self.age * game.speed  / 31_557_600 * 10) / 10} an"
            game.write(text, (20, y - 20), BLUE, 2)
        else:
            text = f"Age : {round(self.age * game.speed  / 31_557_600 * 10) / 10} ans"
            game.write(text, (20, y - 20), BLUE, 2)

        text = f"Masse : {self.mass:.2e} t"
        game.write(text, (20, y - 20), BLUE, 3)

        text = f"Rayon : {round(self.radius * 10) / 10} m"
        game.write(text, (20, y - 20), BLUE, 4)

        text = f"Volume : {self.volume:.2e} m³"
        game.write(text, (20, y - 20), BLUE, 5)

        text = f"Energie cinétique : {self.speed_power():.2e} J"
        game.write(text, (20, y - 20), BLUE, 7)

        text = f"Force subie : {math.sqrt(self.printed_force[0] ** 2 + self.printed_force[1] ** 2):.2e} N"
        game.write(text, (20, y - 20), BLUE, 8)

        text = f"Vitesse : {self.speed:.2e} m/s"
        game.write(text, (20, y - 20), BLUE, 10)

        text = f"Coordonnées : {int(self.x)}; {int(self.y)}"
        game.write(text, (20, y - 20), BLUE, 11)

        nearest_tuple = self.get_nearest()
        if nearest_tuple is not None:
            text = f"Corps le plus proche : n°{nearest_tuple[0]} -> {round(nearest_tuple[1]):.2e} m"
            game.write(text, (20, y - 20), BLUE, 13)
        else:
            text = f"Corps le plus proche : n°Aucun"
            game.write(text, (20, y - 20), BLUE, 13)

    def reset_force_list(self):
        self.attract_forces = []

    def attract(self, other, effective: bool = True) -> tuple[float, float]:
        dx = other.x - float(self.x)
        dy = other.y - float(self.y)

        distance = float(rac2((dx ** 2) + (dy ** 2)))

        if distance <= self.radius + other.radius:
            return 0, 0

        # force = game.gravity * ((self.mass * 1_000_000 * other.mass * 1_000_000) / (distance ** 2)) / 100
        force = game.gravity * ((self.mass * other.mass) / (distance ** 2)) # / 100
        angle = atan2(dy, dx)

        # force
        fx = cos(angle) * force
        fy = sin(angle) * force
        if game.reversed_gravity:
            fx *= -1
            fy *= -1

        if effective:
            # velocity
            self.vx += fx / self.mass
            self.vy += fy / self.mass

        return fx, fy

    @staticmethod
    def correct_latency(speed: float) -> float:
        final_speed = speed * 100 * (1 / game.frequency)
        return final_speed

    def update(self):
        # real force
        self.force = [0.0, 0.0]
        for f in self.attract_forces:
            self.force[0] += f[0]
            self.force[1] += f[1]

        self.force[0] /= len(self.attract_forces) if len(self.attract_forces) != 0 else 1
        self.force[1] /= len(self.attract_forces) if len(self.attract_forces) != 0 else 1

        # printed force
        self.printed_force = [0.0, 0.0]
        for f in self.attract_forces:
            self.printed_force[0] += f[0] / game.gravity * game.G
            self.printed_force[1] += f[1] / game.gravity * game.G

        self.printed_force[0] /= len(self.attract_forces) if len(self.attract_forces) != 0 else 1
        self.printed_force[1] /= len(self.attract_forces) if len(self.attract_forces) != 0 else 1


        if not self.is_born and self in circles:
            self.birthday = game.net_age()

            if game.random_mode:
                self.vx = random.uniform(-1 * math.sqrt(2 * game.random_field / self.mass),
                                         math.sqrt(2 * game.random_field / self.mass))
                self.vy = random.uniform(-1 * math.sqrt(2 * game.random_field / self.mass),
                                         math.sqrt(2 * game.random_field / self.mass))

            self.is_born = True

        if self.birthday is not None:
            self.age = game.net_age() - self.birthday

        self.surface = 4 * self.radius ** 2 * math.pi
        self.volume = 4 / 3 * math.pi * self.radius ** 3

        if not self in circles:
            self.is_selected = False

        self.speed = rac2(self.vx ** 2 + self.vy ** 2) * game.FPS

        self.x += self.correct_latency(self.vx * game.speed)
        self.y += self.correct_latency(self.vy * game.speed)

        self.pos = (self.x, self.y)

    def update_fusion(self, other):
        dx = other.x - float(self.x)
        dy = other.y - float(self.y)

        # Pythagore
        distance = float(rac2((dx ** 2) + (dy ** 2)))

        if game.fusions:
            if self.mass >= other.mass and distance <= self.radius:
                self.fusion(other)

    def fusion(self, other):
        self.x = float((self.x * self.mass + other.x * other.mass) / (self.mass + other.mass))
        self.y = float((self.y * self.mass + other.y * other.mass) / (self.mass + other.mass))

        self.vx = float((self.vx * self.mass + other.vx * other.mass) / (self.mass + other.mass))
        self.vy = float((self.vy * self.mass + other.vy * other.mass) / (self.mass + other.mass))

        self.mass = self.mass + other.mass
        self.radius = rac3(self.mass)

        other.suicide = True

    def is_colliding_with(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        # Pythagore
        distance = rac2((dx ** 2) + (dy ** 2))

        return distance <= self.radius + other.radius


# -----------------
# class Game
# -----------------
class Game:
    def __init__(self):
        # parametres {

        """
        Touches:
            - Espace -> faire pause/depause
            - Molette (facultatif) -> crée les plus petits cops possibles
            - V -> activer/desactiver les vecteurs de vitesse
            - R -> activer/desactiver le random_mode
            - G -> activer/desactiver la gravité inversé
            - Clique droit/gauche/molette -> maintenir pour faire apparaitre des corps
                                          -> selectionner/deselectionner un corps
            - Suppr -> Supprimer un corps selectionné

        """

        self.FULLSCREEN = True

        WIDTH: int = 0  # } <- seulement dans le cas ou FULLSCREEN est desactive
        HEIGHT: int = 0  # }

        self.used_font = 'font.ttf'  # <- fichier en .ttf pour la police d'ecriture

        self.FPS = 120

        self.txt_size = 30  # } pour modifier la taille du texte selon les dimentions de l'ecran
        self.txt_gap: int = 15  # }

        self.speed = 1_000_000_00
        self.growing_speed = 0.5

        self.screen_mode: str = "dark"
        self.music = False
        self.fusions = True

        self.G = 6.6743 * 10 ** -11
        self.default_gravity = 2
        self.gravity: float = self.default_gravity  # } peut etre remplacé par G. ps: c'est lent (très)

        self.strength_vectors = True
        self.cardinals_vectors = False
        self.vectors_in_front = True
        self.vector_length = 1

        self.random_environment_number: int = 20

        self.random_field = 0.01  # <- en TJoules
        # }

        self.info = pygame.display.Info()
        screen_size: tuple[int, int] = (self.info.current_w, self.info.current_h)
        if self.FULLSCREEN:
            self.screen = pygame.display.set_mode(screen_size)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption('Gravity Engine')

        self.is_paused = False
        self.vectors_printed = False

        self.random_mode = False

        self.reversed_gravity = False

        self.temp_FPS = self.FPS

        self.font = pygame.font.Font(self.used_font, self.txt_size)
        self.texts: list = []

        self.music_volume = 1

        self.circle_number = 0

        self.circle_selected = False

        self.beginning_hour = time.time()
        self.time_in_pause = 0

        self.pause_beginning = None

        self.info_y: int = 20

        self.save_time_1 = 0
        self.save_time_2 = 0

        self.frequency = self.FPS
        self.latency = None

        self.camera = Camera(5, 5)

        self.inputs: dict = {}

        self.counter = 0
        
        # Initialiser le gestionnaire GPU
        self.gpu_manager = GPUDataManager()
        self.gpu_manager.initialize_arrays()

    def handle_input(self, event: pygame.event = None) -> None:
        if event.type is pygame.KEYDOWN:
            self.inputs[event.key] = True
            return None

        elif event.type is pygame.KEYUP:
            self.inputs[event.key] = True
            return None

        else:
            return None

    def refresh_pause(self):
        self.time_in_pause += time.time() - self.pause_beginning
        self.pause_beginning = time.time()

    def pause(self):
        self.pause_beginning = time.time()
        self.is_paused = True

    def unpause(self):
        for circle in circles:
            circle.time_in_pause += time.time() - self.pause_beginning

        self.time_in_pause += time.time() - self.pause_beginning

        self.pause_beginning = None
        self.is_paused = False

    def write(self,
              text: str = "[text]",
              dest: tuple[int, int] = (0, 0),
              color: tuple[int, int, int] = (255, 255, 255),
              line: int = 0) -> pygame.Rect | None:

        written = self.font.render(text, 1, color)
        rect = self.screen.blit(written, dest=(dest[0], dest[1] + line * (self.txt_gap + self.txt_size)))
        return rect

    @staticmethod
    def heaviest() -> tuple | None:
        circles_mass = []

        if len(circles) != 0:

            for circle in circles:
                circles_mass.append(circle.mass)

            index = circles_mass.index(max(circles_mass))
            circle_id = circles[index].number

            return circle_id, max(circles_mass)

        else:
            return None

    @staticmethod
    def oldest() -> tuple | None:
        circles_age = []

        if len(circles) != 0:

            for circle in circles:
                circles_age.append(circle.age)

            index = circles_age.index(max(circles_age))
            circle_id = circles[index].number

            return circle_id, max(circles_age)

        else:
            return None

    @staticmethod
    def mass_sum() -> int:
        all_mass = 0

        for circle in circles:
            all_mass += circle.mass

        return all_mass

    def brut_age(self) -> float | None:
        age = time.time() - self.beginning_hour
        return age

    def net_age(self) -> float | None:
        age = self.brut_age() - self.time_in_pause
        return age

    def select_circle(self, number: int) -> None:
        for circle in circles:
            if circle.number == number:
                circle.is_selected = True
                self.circle_selected = True
                return None
        Text(f"Le corps n°{number} n'existe pas", 3)
        return None

    def print_global_info(self, y):
        heaviest_tuple = self.heaviest()

        if heaviest_tuple is not None:
            text = f"Corps le plus lourd : n°{heaviest_tuple[0]} -> {heaviest_tuple[1] / 1000:.2e} t"
            self.write(text, (20, y), BLUE, 2)
        else:
            text = f"Corps le plus lourd : n°Aucun"
            self.write(text, (20, y), BLUE, 2)

        text = "(Ce logiciel inclue un système de correction des FPS)"
        advertisement_printable: bool = heaviest_tuple is not None and self.screen.get_width() - \
                                        self.font.size(f"Gravité inversée (G) : Désactivée")[0] - self.font.size(
            f"Corps le plus lourd : n°{heaviest_tuple[0]} -> {int(heaviest_tuple[1] * 10) / 10} t")[0] > \
                                        self.font.size(text)[0]
        if advertisement_printable:
            self.write(text, (int((self.screen.get_width() / 2) - (self.font.size(text)[0] / 2)), y), BLUE, 0)

        if self.circle_selected and len(circles) > 0:
            self.write(f"Détruire : Suppr", (
                int((self.screen.get_width() / 2) - (self.font.size("Détruire : Suppr")[0] / 2)),
                y + self.txt_size + self.txt_gap), BLUE, 0)

        if self.reversed_gravity:
            text = f"Gravité inversée (G) : Activée"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 0)
        else:
            text = f"Gravité inversée (G) : Désactivée"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 0)

        if self.vectors_printed:
            text = f"Vecteurs (V) : Activés"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 1)
        else:
            text = f"Vecteurs (V) : Désactivés"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 1)

        if self.random_mode:
            text = f"Mode aléatoire (R) : Activé"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 2)
        else:
            text = f"Mode aléatoire (R) : Désactivé"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 2)

        text = f"Structure aléatoire ({self.random_environment_number} corps) : P"
        self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]), y), BLUE, 4)

        text = f"Accéleration : ×{self.speed:.2e}"
        self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                          self.screen.get_height() - 20 - 2 * self.txt_size - self.txt_gap), BLUE, 0)

        if self.is_paused:
            text = f"Pause (Espace) : Activée"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                              self.screen.get_height() - 20 - self.txt_size), BLUE, 0)
        else:
            text = f"Pause (Espace) : Désactivée"
            self.write(text, (self.screen.get_width() - 20 - (self.font.size(text)[0]),
                              self.screen.get_height() - 20 - self.txt_size), BLUE, 0)

        text = f"Nombre de corps : {len(circles)}"
        self.write(text, (20, y), BLUE, 0)

        text = f"Masse totale : {round(self.mass_sum() / 1000) / 1000} kt"
        self.write(text, (20, y), BLUE, 1)

        oldest_tuple = self.oldest()
        if oldest_tuple is not None:
            if oldest_tuple[1] * game.speed  / 31_557_600 < 2:
                text = f"Corps le plus vieux : n°{oldest_tuple[0]} -> {int(oldest_tuple[1] * game.speed  / 31_557_600 * 10) / 10} an"
                self.write(text, (20, y), BLUE, 3)
            else:
                text = f"Corps le plus vieux : n°{oldest_tuple[0]} -> {int(oldest_tuple[1] * game.speed  / 31_557_600 * 10) / 10} ans"
                self.write(text, (20, y), BLUE, 3)
        else:
            text = f"Corps le plus vieux : n°Aucun"
            self.write(text, (20, y), BLUE, 3)

        if self.net_age() * game.speed / 31_557_600 < 2:
            text = f"Age de la simulation : {int(self.net_age() * game.speed / 31_557_600 * 10) / 10} an"
            self.write(text, (20, self.screen.get_height() - 20 - game.txt_size), BLUE, 0)
        else:
            text = f"Age de la simulation : {int(self.net_age() * game.speed  / 31_557_600 * 10) / 10} ans"
            self.write(text, (20, self.screen.get_height() - 20 - game.txt_size), BLUE, 0)

        text = f"FPS : {round(self.temp_FPS)}"
        self.write(text, (int((self.screen.get_width() / 2) - (self.font.size(text)[0] / 2)),
                          int(self.screen.get_height() - 20 - game.txt_size)), BLUE, 0)

    def generate_environment(self, count: int = 50):
        for c in range(count):
            new = Circle(x=random.uniform(0, self.screen.get_width()),
                         y=random.uniform(0, self.screen.get_height()),
                         radius=0.1,
                         mass=1)
            circles.append(new)

    def get_frequency(self) -> float | None:
        frequency = 1 / self.get_latency()
        self.save_time_1 = time.time()
        return frequency

    def get_latency(self) -> float | None:
        latency = time.time() - self.save_time_2
        self.save_time_2 = time.time()
        return latency

    # noinspection PyGlobalUndefined
    def run(self):
        pygame.mixer.music.set_volume(self.music_volume)

        global circles
        circles = []

        temp_circle = None
        mouse_down = False

        clock = pygame.time.Clock()

        self.circle_selected = False
        
        # Réinitialiser le gestionnaire GPU
        self.gpu_manager = GPUDataManager()
        self.gpu_manager.initialize_arrays()

        running = True
        while running:
            for text in self.texts:
                if time.time() - text.birthday >= text.duration:
                    self.texts.remove(text)
                else:
                    text.update()

            if self.counter == 0 or self.counter == int(self.FPS / 2):
                self.temp_FPS = self.frequency

            if self.counter + 1 >= self.FPS:
                self.counter = 0
            else:
                self.counter += 1

            if self.camera is not None:
                self.camera.update_visual()

            self.frequency = self.get_frequency()
            self.latency = self.get_latency()

            for circle in circles:
                if circle.is_selected:
                    self.circle_selected = True
                    for other in circles:
                        if circle != other:
                            other.is_selected = False
                    break
                else:
                    self.circle_selected = False

            if self.screen_mode == "dark":
                self.screen.fill(BLACK)

            elif self.screen_mode == "light":
                self.screen.fill(WHITE)

            if not pygame.mixer.music.get_busy() and self.music is True:
                try:
                    pygame.mixer.music.load('music1.mp3')
                    pygame.mixer.music.queue('music2.mp3')
                    pygame.mixer.music.queue('music3.mp3')
                except FileNotFoundError:
                    pass

                pygame.mixer.music.play(0, 0, 1)

            for event in pygame.event.get():
                self.handle_input(event)
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    circle_collided = None
                    can_create_circle = False
                    mouse_down = True
                    x, y = pygame.mouse.get_pos()
                    if len(circles) > 0:
                        for circle in circles:
                            if circle.rect is not None:
                                if circle.rect.collidepoint(event.pos):
                                    circle_collided = circle.number
                                    for c in circles:
                                        if c != circle:
                                            c.is_selected = False
                                    break

                        if circle_collided is not None:
                            for circle in circles:
                                if circle.number == circle_collided:
                                    circle.switch_selection()
                                    break

                        elif self.circle_selected:
                            for circle in circles:
                                circle.is_selected = False
                        else:
                            can_create_circle = True

                        if can_create_circle:
                            temp_circle = Circle(x, y, 3, 1)
                            #can_create_circle = False  <- useless
                    else:
                        temp_circle = Circle(x, y, 3, 1)

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False
                    if temp_circle is not None:
                        circles.append(temp_circle)
                        # Ajouter le cercle au gestionnaire GPU
                        idx = len(circles) - 1
                        self.gpu_manager.add_circle(temp_circle, idx)
                        temp_circle = None

                # clavier {
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_SPACE:
                        if self.is_paused:
                            self.unpause()
                        else:
                            self.pause()

                    elif event.key == pygame.K_v:
                        if self.vectors_printed:
                            self.vectors_printed = False
                        else:
                            self.vectors_printed = True

                    elif event.key == pygame.K_r:
                        if self.random_mode:
                            self.random_mode = False
                        else:
                            self.random_mode = True

                    elif event.key == pygame.K_g:
                        if self.reversed_gravity:
                            self.reversed_gravity = False
                        else:
                            self.reversed_gravity = True

                    elif event.key == pygame.K_p:
                        old_count = len(circles)
                        self.generate_environment(count=self.random_environment_number)
                        # Ajouter les nouveaux cercles au gestionnaire GPU
                        for i in range(old_count, len(circles)):
                            self.gpu_manager.add_circle(circles[i], i)
                    # }

                    for circle in circles:
                        if circle.is_selected and event.key == pygame.K_DELETE:
                            circles.remove(circle)

            if mouse_down and temp_circle:
                temp_circle.radius += self.growing_speed * 100 * (1 / self.frequency)
                temp_circle.mass = temp_circle.radius ** 3
                collision_detected = False
                for circle in circles:
                    if temp_circle.is_colliding_with(circle):
                        collision_detected = True
                        break

                if collision_detected:
                    circles.append(temp_circle)
                    # Ajouter le cercle au gestionnaire GPU
                    idx = len(circles) - 1
                    self.gpu_manager.add_circle(temp_circle, idx)
                    temp_circle = None
                    mouse_down = False

            # Mettre à jour les arrays GPU avec les nouveaux cercles
            for i, circle in enumerate(circles):
                if circle not in self.gpu_manager.circle_to_index:
                    self.gpu_manager.add_circle(circle, i)
                else:
                    self.gpu_manager.update_circle_to_gpu(circle)
            
            # Mettre à jour current_size
            self.gpu_manager.current_size = len(circles)
            
            # Retirer les cercles supprimés
            for circle in circles[:]:
                if circle.suicide is True:
                    self.gpu_manager.remove_circle(circle)
                    circles.remove(circle)

            if self.is_paused:
                self.refresh_pause()

            else:
                # Calculs sur GPU
                dt = 1.0 / self.frequency if self.frequency > 0 else 1.0 / self.FPS
                
                # Calculer toutes les forces gravitationnelles sur GPU
                self.gpu_manager.compute_gravity_forces(
                    self.gravity, 
                    self.reversed_gravity, 
                    dt
                )
                
                # Vérifier les collisions et fusions sur GPU
                if self.fusions:
                    self.gpu_manager.check_collisions_and_fusions(circles)
                
                # Synchroniser les données GPU vers CPU pour l'affichage
                for circle in circles:
                    if circle in self.gpu_manager.circle_to_index:
                        idx = self.gpu_manager.circle_to_index[circle]
                        self.gpu_manager.update_circle_from_gpu(circle)
                        
                        # Récupérer les forces depuis GPU
                        if GPU_AVAILABLE and self.gpu_manager.xp is cp and hasattr(cp, 'asnumpy'):
                            circle.force[0] = float(cp.asnumpy(self.gpu_manager.forces_x[idx]))
                            circle.force[1] = float(cp.asnumpy(self.gpu_manager.forces_y[idx]))
                        else:
                            circle.force[0] = float(self.gpu_manager.forces_x[idx])
                            circle.force[1] = float(self.gpu_manager.forces_y[idx])
                        
                        # Calculer printed_force
                        circle.printed_force[0] = circle.force[0] / self.gravity * self.G if self.gravity != 0 else 0
                        circle.printed_force[1] = circle.force[1] / self.gravity * self.G if self.gravity != 0 else 0
                        
                        # Mettre à jour les propriétés calculées
                        circle.speed = rac2(circle.vx ** 2 + circle.vy ** 2) * self.FPS
                        circle.surface = 4 * circle.radius ** 2 * math.pi
                        circle.volume = 4 / 3 * math.pi * circle.radius ** 3
                        circle.pos = (circle.x, circle.y)
                
                # Mettre à jour les âges et autres propriétés non-GPU
                for circle in circles:
                    if not circle.is_born and circle in circles:
                        circle.birthday = self.net_age()
                        if self.random_mode:
                            circle.vx = random.uniform(-1 * math.sqrt(2 * self.random_field / circle.mass),
                                                       math.sqrt(2 * self.random_field / circle.mass))
                            circle.vy = random.uniform(-1 * math.sqrt(2 * self.random_field / circle.mass),
                                                       math.sqrt(2 * self.random_field / circle.mass))
                            self.gpu_manager.update_circle_to_gpu(circle)
                        circle.is_born = True
                    
                    if circle.birthday is not None:
                        circle.age = self.net_age() - circle.birthday

            # now = time.time()
            if self.vectors_in_front:
                for circle in circles:
                    circle.draw(self.screen)
                if self.vectors_printed:
                    for circle in circles:
                        if self.strength_vectors:
                            circle.PrintStrengthV(False)
                        circle.print_GSV(False)

            else:
                if self.vectors_printed:
                    for circle in circles:
                        if self.strength_vectors:
                            circle.PrintStrengthV(False)
                        circle.print_GSV(False)
                for circle in circles:
                    circle.draw(self.screen)

            if temp_circle:
                temp_circle.draw(self.screen)
            # print(f"Affichage : {time.time() - now}")

            self.print_global_info(self.info_y)
            for circle in circles:
                if circle.is_selected:
                    circle.print_info(circle.info_y)
                    pass

            for circle in circles:
                circle.reset_force_list()

            pygame.display.flip()
            clock.tick(self.FPS)

        pygame.quit()
        sys.exit('See you soon !')


# -----------------
# Engine
# -----------------
if __name__ == '__main__':
    pygame.init()
    # colors
    WHITE = (255, 255, 255)
    BLUE = (10, 124, 235)
    SP_BLUE = (130, 130, 220)
    BLACK = (0, 0, 0)
    DUCKY_GREEN = (28, 201, 89)
    GREEN = (0, 255, 0)
    YELLOW = (241, 247, 0)
    DARK_GREY = (100, 100, 100)
    RED = (255, 0, 0)

    circles: list[Circle] = []

    game = Game()
    game.run()
