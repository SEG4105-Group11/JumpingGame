from projectile import Projectile
import random


class Projectiles:
    MIN_DISTANCE = 200
    MAX_DISTANCE = 250

    def __init__(self):
        self.projectiles = []

    def add_projectile(self, p):
        self.projectiles.append(p)

    def remove_projectile(self, p):
        self.projectiles.remove(p)

    def move_projectiles(self):
        for p in self.projectiles:
            if p.is_off_screen():
                self.remove_projectile(p)
            else:
                p.move()

    def create_next(self, prev, screenwidth):
        distance = random.randint(Projectiles.MIN_DISTANCE, Projectiles.MAX_DISTANCE)
        if prev.x + distance - Projectile.RADIUS <= screenwidth:
            next_projectile = Projectile(prev.x + distance, prev.y)
            self.add_projectile(next_projectile)
            prev = next_projectile

        return prev
