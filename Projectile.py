import random

class Projectile:
    projectiles = []
    radius = 10
    velocity = 10
    distance = random.randint(200, 250)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_projectile(self, p):
        Projectile.projectiles.append(p)

    def remove_projectile(self, p):
        Projectile.projectiles.remove(p)

    def is_offscreen(self):
        return self.x <= Projectile.radius

    def move_projectiles(self):
        for p in Projectile.projectiles:
            if p.is_offscreen():
                p.remove_projectile(p)
            else:
                p.x = p.x - Projectile.velocity

    def create_next(self, prev, screenwidth):
        if prev.x + Projectile.distance + Projectile.radius < screenwidth:
            next = Projectile(prev.x + Projectile.distance, prev.y)
            next.add_projectile(next)
            prev = next

        return prev


    def is_collision(self, char):
        if (((char.x + char.width - self.x)**2) + ((char.y - self.y)**2)) < Projectile.radius ** 2:
            return True
        if (((char.x - self.x) ** 2) + ((char.y - self.y) ** 2)) < Projectile.radius ** 2:
            return True
        if (self.y + Projectile.radius <= char.y <= self.y - Projectile.radius) and (self.x - Projectile.radius <= char.x <= self.x + Projectile.radius):
            return True

        return False
