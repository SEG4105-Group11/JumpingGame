import globals


class Polygon:
    # Square
    LENGTH = 20
    VELOCITY = 5

    def __init__(self, c1, c2, c3, c4, lvl):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.lvl = lvl
        self.should_grow_up = True

    def is_collision(self, char):
        return (char.y + char.height >= self.c2[1]) and (
            char.x + char.width >= self.c1[0] and char.x <= self.c4[0]
        )

    def is_off_screen(self):
        return self.c4[0] <= 0

    def move(self):
        if self.lvl == "Pixel Monsters":
            self.c1 = (self.c1[0] - Polygon.VELOCITY, self.c1[1])
            self.c2 = (
                self.c2[0] - Polygon.VELOCITY,
                self.c2[1]
                - (Polygon.VELOCITY if self.should_grow_up else -Polygon.VELOCITY),
            )
            self.c3 = (
                self.c3[0] - Polygon.VELOCITY,
                self.c3[1]
                - (Polygon.VELOCITY if self.should_grow_up else -Polygon.VELOCITY),
            )
            self.c4 = (self.c4[0] - Polygon.VELOCITY, self.c4[1])

            if self.c2[1] < (globals.SCREENHEIGHT - 2 * Polygon.LENGTH) or (
                self.c2[1] >= (globals.SCREENHEIGHT - Polygon.LENGTH)
                and not self.should_grow_up
            ):
                self.should_grow_up = not self.should_grow_up
        else:
            self.c1 = (self.c1[0] - Polygon.VELOCITY, self.c1[1])
            self.c2 = (self.c2[0] - Polygon.VELOCITY, self.c2[1])
            self.c3 = (self.c3[0] - Polygon.VELOCITY, self.c3[1])
            self.c4 = (self.c4[0] - Polygon.VELOCITY, self.c4[1])
