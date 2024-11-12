import math


class Projectile:
    RADIUS = 10
    VELOCITY = 10

    SIN_AMPLITUDE: float = 10
    SIN_FREQ: float = 2

    def __init__(self, x, y, type=None):
        self.x = x
        self.start_y = y
        self.y = y
        self.type = type

    def is_off_screen(self):
        return self.x <= Projectile.RADIUS

    def move(self):
        self.x = self.x - Projectile.VELOCITY
        if self.type == "sine":
            self.y = self.start_y + Projectile.SIN_AMPLITUDE * math.sin(
                Projectile.SIN_FREQ * math.radians(self.x)
            )
        elif self.type == "cosine":
            self.y = self.start_y + Projectile.SIN_AMPLITUDE * math.cos(
                Projectile.SIN_FREQ * math.radians(self.x)
            )

    def is_collision(self, char):
        if (
            char.x - Projectile.RADIUS
            <= self.x - Projectile.RADIUS
            <= char.x + char.width
        ) and (
            char.y
            <= self.y + Projectile.RADIUS
            <= char.y + char.height + Projectile.RADIUS
        ):
            return True

        return False
