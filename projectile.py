class Projectile:
    RADIUS = 10
    VELOCITY = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_off_screen(self):
        return self.x <= Projectile.RADIUS

    def move(self):
        self.x = self.x - Projectile.VELOCITY

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
