class Polygon:
    # Square
    polygons = []
    length = 20

    def __init__(self, c1, c2, c3, c4, collision=False):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.collision = collision

    def is_collision(self, bl, br):
        return (bl[1] >= self.c2[1]) and (br[0] >= self.c1[0] and bl[0] <= self.c4[0])

    def add_polygon(self, p):
        self.polygons.append(p)

    def remove_polygon(self, p):
        self.polygons.remove(p)
