from Polygon import Polygon
import random


class Polygons:
    MIN_DISTANCE = 200
    MAX_DISTANCE = 250

    def __init__(self):
        self.polygons = []

    def add_polygon(self, p):
        self.polygons.append(p)

    def remove_polygon(self, p):
        self.polygons.remove(p)

    def move_polygons(self):
        for p in self.polygons:
            if p.is_off_screen():
                self.remove_polygon(p)
            else:
                p.move()

    def create_next(self, prev, screenwidth):
        distance = random.randint(Polygons.MIN_DISTANCE, Polygons.MAX_DISTANCE)
        coord1 = (prev.c1[0] + distance, prev.c1[1])
        coord2 = (prev.c2[0] + distance, prev.c2[1])
        coord3 = (prev.c3[0] + distance, prev.c3[1])
        coord4 = (prev.c4[0] + distance, prev.c4[1])

        if coord4[0] <= screenwidth:
            next_polygon = Polygon(coord1, coord2, coord3, coord4)
            self.add_polygon(next_polygon)
            prev = next_polygon

        return prev
