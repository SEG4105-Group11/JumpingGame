class Polygon:
    # Square
    polygons = []
    length = 20
    vel = 5

    def __init__(self, c1, c2, c3, c4, offscreen=False):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.offscreen = offscreen

    def is_collision(self, bl, br):
        return (bl[1] >= self.c2[1]) and (br[0] >= self.c1[0] and bl[0] <= self.c4[0])

    def add_polygon(self, p):
        self.polygons.append(p)

    def remove_polygon(self, p):
        self.polygons.remove(p)

    def is_offscreen(self, d):
        self.offscreen = self.c4[0] - d <= 0
        return self.offscreen
