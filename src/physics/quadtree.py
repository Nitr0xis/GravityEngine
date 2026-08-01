from math import sqrt, atan2, cos, sin


class QuadNode:
    __slots__ = ("cx", "cy", "half", "mass", "com_x", "com_y",
                 "children", "bodies", "is_leaf")

    def __init__(self, cx, cy, half):
        self.cx, self.cy, self.half = cx, cy, half
        self.mass = 0.0
        self.com_x = 0.0
        self.com_y = 0.0
        self.children = None
        self.bodies = []       # liste des corps si feuille (1 en temps normal)
        self.is_leaf = True

    def _quadrant_index(self, x, y):
        idx = 0
        if x > self.cx:
            idx |= 1
        if y > self.cy:
            idx |= 2
        return idx

    def _child_bounds(self, idx):
        q = self.half / 2
        dx = q if idx & 1 else -q
        dy = q if idx & 2 else -q
        return self.cx + dx, self.cy + dy, q

    def _accumulate(self, body):
        total_mass = self.mass + body.mass
        self.com_x = (self.com_x * self.mass + body.x * body.mass) / total_mass
        self.com_y = (self.com_y * self.mass + body.y * body.mass) / total_mass
        self.mass = total_mass

    def insert(self, body):
        if self.children is not None:
            self._accumulate(body)
            self._insert_into_child(body)
            return

        if not self.bodies:
            self.bodies.append(body)
            self.mass = body.mass
            self.com_x, self.com_y = body.x, body.y
            return

        # Critère d'arrêt physique : si ce nœud est déjà plus petit que le
        # rayon des corps qu'il contient, subdiviser davantage n'a plus de
        # sens géométrique (les corps occupent déjà toute la cellule).
        # On les garde ensemble dans une feuille "dense", traitée en exact
        # (pairwise) lors du calcul de force — coût négligeable car cette
        # situation ne concerne que des corps quasi-superposés.
        smallest_radius = min(b.radius for b in self.bodies + [body])
        if self.half <= max(smallest_radius, 1e-9):
            self._accumulate(body)
            self.bodies.append(body)
            return

        # Sinon : subdivision normale
        old_bodies = self.bodies
        self.bodies = []
        self.children = [None, None, None, None]
        self.is_leaf = False
        for b in old_bodies:
            self._insert_into_child(b)

        self._accumulate(body)
        self._insert_into_child(body)

    def _insert_into_child(self, body):
        idx = self._quadrant_index(body.x, body.y)
        if self.children[idx] is None:
            cx, cy, half = self._child_bounds(idx)
            self.children[idx] = QuadNode(cx, cy, half)
        self.children[idx].insert(body)

    def compute_force(self, on_body, theta, G, reversed_gravity):
        if self.mass == 0.0:
            return 0.0, 0.0

        if self.children is None:
            # Feuille : somme exacte sur les (rares) corps qu'elle contient
            fx_total, fy_total = 0.0, 0.0
            for other in self.bodies:
                if other is on_body:
                    continue
                dx = other.x - on_body.x
                dy = other.y - on_body.y
                distance = sqrt(dx * dx + dy * dy)
                if distance <= on_body.radius + other.radius:
                    continue
                force = G * (on_body.mass * other.mass) / (distance ** 2)
                angle = atan2(dy, dx)
                fx, fy = cos(angle) * force, sin(angle) * force
                if reversed_gravity:
                    fx, fy = -fx, -fy
                fx_total += fx
                fy_total += fy
            return fx_total, fy_total

        dx = self.com_x - on_body.x
        dy = self.com_y - on_body.y
        distance = sqrt(dx * dx + dy * dy)
        if distance < 1e-9:
            distance = 1e-9

        if (self.half * 2 / distance) < theta:
            force = G * (on_body.mass * self.mass) / (distance ** 2)
            angle = atan2(dy, dx)
            fx, fy = cos(angle) * force, sin(angle) * force
            if reversed_gravity:
                fx, fy = -fx, -fy
            return fx, fy

        fx_total, fy_total = 0.0, 0.0
        for child in self.children:
            if child is not None:
                cfx, cfy = child.compute_force(on_body, theta, G, reversed_gravity)
                fx_total += cfx
                fy_total += cfy
        return fx_total, fy_total


def build_quadtree(circles):
    if not circles:
        return None
    xs = [c.x for c in circles]
    ys = [c.y for c in circles]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    half = max(max_x - min_x, max_y - min_y, 1.0) / 2 * 1.001
    root = QuadNode(cx, cy, half)
    for c in circles:
        root.insert(c)
    return root
    