import itertools
import pygame
import globals
from timer import Timer
from projectile import Projectile
from projectiles import Projectiles
from polygon import Polygon
from polygons import Polygons
from character import Character


# REFERENCE: https://github.com/kidscancode/gamedev/blob/master/tutorials/examples/shake.py#L27
# this function creates our shake-generator
# it "moves" the screen to the left and right
# three times by yielding (-5, 0), (-10, 0),
# ... (-20, 0), (-15, 0) ... (20, 0) three times,
# then keeps yielding (0, 0)
def shake():
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield (x * s, 0)
        for x in range(20, 0, 5):
            yield (x * s, 0)
        s *= -1
    while True:
        yield (0, 0)


class Game:

    # (lives, block_velocity_multiplier, projectile_velocity_multiplier)
    difficulty_parameters = {
        "easy": (10, 0.5, 0.5),
        "medium": (5, 1, 1),
        "hard": (3, 1.5, 1.5),
        "god": (1, 2, 2),
    }

    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("images/bg.jpg")
        self.difficulty = None
        self.timer = Timer()
        self.offset = itertools.repeat((0, 0))

    def pause(self):
        self.timer.pause()

    def resume(self):
        self.timer.resume()

    def initialize(self):
        assert (
            self.difficulty is not None
        ), "Tried to initialize game without difficulty"

        # Polygon setup
        Polygon.VELOCITY *= self.difficulty_parameters[self.difficulty][1]
        self.polygons = Polygons()
        first_polygon = Polygon(
            (globals.SCREENWIDTH // 3, globals.SCREENHEIGHT),
            (globals.SCREENWIDTH // 3, globals.SCREENHEIGHT - Polygon.LENGTH),
            (
                globals.SCREENWIDTH // 3 + Polygon.LENGTH,
                globals.SCREENHEIGHT - Polygon.LENGTH,
            ),
            (globals.SCREENWIDTH // 3 + Polygon.LENGTH, globals.SCREENHEIGHT),
        )
        self.polygons.add_polygon(first_polygon)
        self.previous_polygon = first_polygon
        self.collided_polygons = []
        self.polygon_lost_lives = []

        # Projectile setup
        Projectile.VELOCITY *= self.difficulty_parameters[self.difficulty][2]
        self.projectiles = Projectiles()
        first_projectile = Projectile(
            globals.SCREENWIDTH - Projectile.RADIUS,
            globals.SCREENHEIGHT - 2 * Character.height,
        )
        self.projectiles.add_projectile(first_projectile)
        self.previous_projectile = first_projectile
        self.collided_projectiles = []
        self.projectile_lost_lives = []

        # Character setup
        self.char = Character(0, globals.SCREENHEIGHT - Character.height)
        self.char.set_lives(self.difficulty_parameters[self.difficulty][0])

        # Game music setup
        pygame.mixer.music.load(f"audio/{self.difficulty}.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 3)
        self.collision_sound = pygame.mixer.Sound("audio/collision.mp3")

        self.timer.start()

    def draw_game(self):
        self.window.blit(self.bg, (0, 0))
        self.clock.tick(30)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.char.x - self.char.vel >= 0:
            self.char.move_left()
        elif (
            keys[pygame.K_d]
            and self.char.x + self.char.vel <= globals.SCREENWIDTH - self.char.width
        ):
            self.char.move_right()
        else:
            self.char.set_standing()

        if not self.char.isJump:
            if keys[pygame.K_SPACE]:
                self.char.set_jump()
        else:
            self.char.jump()

        # Create next polygon
        self.previous_polygon = self.polygons.create_next(
            self.previous_polygon, globals.SCREENWIDTH
        )

        # Draw polygons
        for p in self.polygons.polygons:
            pygame.draw.polygon(self.window, (255, 0, 0), [p.c1, p.c2, p.c3, p.c4])

        # Create next projectile
        self.previous_projectile = self.projectiles.create_next(
            self.previous_projectile, globals.SCREENWIDTH
        )

        # Draw projectiles
        for p in self.projectiles.projectiles:
            pygame.draw.circle(self.window, (255, 0, 0), (p.x, p.y), p.RADIUS)

        # Check Projectile collision
        for p in self.projectiles.projectiles:
            if p.is_collision(self.char) and p not in self.collided_projectiles:
                self.collided_projectiles.append(p)

        # Check Polygon collision
        for p in self.polygons.polygons:
            if p.is_collision(self.char) and p not in self.collided_polygons:
                self.collided_polygons.append(p)

        # Decrement lives

        # Check Polygon collision
        for p in self.collided_polygons:
            if p not in self.polygon_lost_lives and self.char.lives - 1 >= 0:
                self.char.lives -= 1
                self.offset = shake()
                pygame.mixer.Sound.play(self.collision_sound)
                self.polygon_lost_lives.append(p)
                self.collided_polygons.remove(p)

        # Check Projectile collision
        for p in self.collided_projectiles:
            if p not in self.projectile_lost_lives and self.char.lives - 1 >= 0:
                self.char.lives -= 1
                self.offset = shake()
                pygame.mixer.Sound.play(self.collision_sound)
                self.projectile_lost_lives.append(p)
                self.collided_projectiles.remove(p)

        # Check lives
        if self.char.lives == 0:
            pygame.mixer.music.stop()
            self.timer.stop()
            globals.global_mode = "gameover"

        # Move polygons
        self.polygons.move_polygons()

        # Move projectiles
        self.projectiles.move_projectiles()

        # Draw character and UI
        if self.char.walk + 1 >= 27:
            self.char.walk = 0
        if self.char.left:
            self.window.blit(
                self.char.walk_left[self.char.walk // 3], (self.char.x, self.char.y)
            )
            self.char.walk += 1
        elif self.char.right:
            self.window.blit(
                self.char.walk_right[self.char.walk // 3], (self.char.x, self.char.y)
            )
            self.char.walk += 1
        else:
            self.window.blit(self.char.char_img, (self.char.x, self.char.y))

        lives_left = globals.font.render(
            "Lives left: " + str(self.char.lives), True, (255, 0, 0)
        )
        text_lives_left = lives_left.get_rect()
        text_size = globals.font.size("Lives left: " + str(self.char.lives))
        text_lives_left.center = (globals.SCREENWIDTH - int(text_size[0] / 2) - 10, 50)
        self.window.blit(lives_left, text_lives_left)

        time_alive = f"{self.timer.get_time():.4}"
        score = globals.font.render("Time Alive: " + time_alive, True, (255, 0, 0))
        text_score = score.get_rect()
        text_size = globals.font.size("Time Alive: " + time_alive)
        text_score.center = (int(text_size[0] / 2) + 10, 50)
        self.window.blit(score, text_score)
