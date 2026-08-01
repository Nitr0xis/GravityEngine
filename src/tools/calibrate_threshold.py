import time
import random
from quadtree import build_quadtree
from forces_manager import compute_forces_vectorized

class FakeCircle:
    def __init__(self, x, y, mass, radius):
        self.x, self.y, self.mass, self.radius = x, y, mass, radius
        self.attract_forces = []

def make_bodies(n):
    return [FakeCircle(random.uniform(0, 1e9), random.uniform(0, 1e9),
                        random.uniform(1e20, 1e26), random.uniform(1e5, 1e7))
            for _ in range(n)]

G = 6.6743e-11
for n in [50, 100, 150, 200, 300, 400, 500, 550, 600, 650, 700, 1000, 1500]:
    bodies = make_bodies(n)

    t0 = time.perf_counter()
    tree = build_quadtree(bodies)
    for b in bodies:
        tree.compute_force(b, 0.5, G, False)
    t_bh = time.perf_counter() - t0

    t0 = time.perf_counter()
    compute_forces_vectorized(bodies, G, False)
    t_np = time.perf_counter() - t0

    winner = "Barnes-Hut" if t_bh < t_np else "NumPy"
    print(f"n={n:5d} | BH: {t_bh*1000:6.2f}ms | NumPy: {t_np*1000:6.2f}ms | -> {winner}")
