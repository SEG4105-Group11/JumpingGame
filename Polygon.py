import random


class Polygon:
    # Square
    polygons = []
    length = 20
    vel = 5
    distance = random.randint(200, 250)

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

    def move_polygons(self):
        for e in Polygon.polygons:
            if e.offscreen:
                e.remove_polygon(e)
            else:
                e.c1 = (e.c1[0] - Polygon.vel, e.c1[1])
                e.c2 = (e.c2[0] - Polygon.vel, e.c2[1])
                e.c3 = (e.c3[0] - Polygon.vel, e.c3[1])
                e.c4 = (e.c4[0] - Polygon.vel, e.c4[1])

    def create_next(self, prev, screen_width):
        coord1 = (prev.c1[0] + Polygon.distance, prev.c1[1])
        coord2 = (prev.c2[0] + Polygon.distance, prev.c2[1])
        coord3 = (prev.c3[0] + Polygon.distance, prev.c3[1])
        coord4 = (prev.c4[0] + Polygon.distance, prev.c4[1])
        if coord4[0] <= screen_width:
            next_polygon = Polygon(coord1, coord2, coord3, coord4)
            next_polygon.add_polygon(next_polygon)
            prev = next_polygon

        return prev
