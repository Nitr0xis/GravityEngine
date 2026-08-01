import math
from collections import defaultdict


class SpatialHashGrid:
    def __init__(self, cell_size: float):
        self.cell_size = max(cell_size, 1e-6)
        self.cells = defaultdict(list)

    def _cell_of(self, x, y):
        return (math.floor(x / self.cell_size), math.floor(y / self.cell_size))

    def insert(self, body):
        self.cells[self._cell_of(body.x, body.y)].append(body)

    def candidates_near(self, body):
        ix, iy = self._cell_of(body.x, body.y)
        result = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                result.extend(self.cells.get((ix + dx, iy + dy), ()))
        return result


def build_collision_grid(circles):
    if not circles:
        return None
    max_radius = max(c.radius for c in circles)
    grid = SpatialHashGrid(cell_size=max(2 * max_radius, 1.0))
    for c in circles:
        grid.insert(c)
    return grid
    