import globals
import highscores
import settings
import utils

import datetime
import itertools
import json
import os
import pygame

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
        "Easy": (10, 0.5, 0.5),
        "Medium": (5, 1, 1),
        "Hard": (3, 1.5, 1.5),
        "God": (1, 2, 2),
    }

    projectile_types = {
        "Night Stars": None,
        "Pixel Monsters": "sine",
        "Scary Wolf": "helix",
    }

    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("images/bg.jpg")
        self.difficulty = None
        self.level = None
        self.timer = Timer()
        self.offset = itertools.repeat((0, 0))

    def pause(self):
        self.timer.pause()

    def resume(self):
        self.timer.resume()

    def reset(self):
        self.difficulty = None
        self.level = None
        self.timer = Timer()
        self.offset = itertools.repeat((0, 0))
        Polygon.VELOCITY = 5
        Projectile.VELOCITY = 10

    def initialize(self):
        assert (
            self.difficulty is not None
        ), "Tried to initialize game without difficulty"

        # Polygon setup
        Polygon.VELOCITY *= self.difficulty_parameters[self.difficulty][1]
        self.polygons = Polygons(self.level)
        first_polygon = Polygon(
            (globals.SCREENWIDTH // 3, globals.SCREENHEIGHT),
            (globals.SCREENWIDTH // 3, globals.SCREENHEIGHT - Polygon.LENGTH),
            (
                globals.SCREENWIDTH // 3 + Polygon.LENGTH,
                globals.SCREENHEIGHT - Polygon.LENGTH,
            ),
            (globals.SCREENWIDTH // 3 + Polygon.LENGTH, globals.SCREENHEIGHT),
            self.level,
        )
        self.polygons.add_polygon(first_polygon)
        self.previous_polygon = first_polygon
        self.collided_polygons = []
        self.polygon_lost_lives = []

        # Projectile setup
        Projectile.VELOCITY *= self.difficulty_parameters[self.difficulty][2]
        self.projectiles = Projectiles(Game.projectile_types[self.level])
        if self.level == "Scary Wolf":
            first_projectile = Projectile(
                globals.SCREENWIDTH - Projectile.RADIUS,
                globals.SCREENHEIGHT - 2 * Character.height,
                type="sine",
            )
            self.projectiles.add_projectile(first_projectile)
            first_projectile = Projectile(
                globals.SCREENWIDTH - Projectile.RADIUS,
                globals.SCREENHEIGHT - 2 * Character.height,
                type="cosine",
            )
            self.projectiles.add_projectile(first_projectile)
        else:
            first_projectile = Projectile(
                globals.SCREENWIDTH - Projectile.RADIUS,
                globals.SCREENHEIGHT - 2 * Character.height,
                type=Game.projectile_types[self.level],
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

        move_left_keys = [
            pygame.key.key_code(k) for k in settings.data.get("Move Left")
        ]
        move_right_keys = [
            pygame.key.key_code(k) for k in settings.data.get("Move Right")
        ]
        jump_keys = [pygame.key.key_code(k) for k in settings.data.get("Jump")]
        if any(keys[k] for k in move_left_keys) and self.char.x - self.char.vel >= 0:
            self.char.move_left()
        elif (
            any(keys[k] for k in move_right_keys)
            and self.char.x + self.char.vel <= globals.SCREENWIDTH - self.char.width
        ):
            self.char.move_right()
        else:
            self.char.set_standing()

        if not self.char.isJump:
            if any(keys[k] for k in jump_keys):
                self.char.set_jump()
        else:
            self.char.jump()

        # Create next polygon
        self.previous_polygon = self.polygons.create_next(
            self.previous_polygon, globals.SCREENWIDTH
        )

        # Draw polygons
        for p in self.polygons.polygons:
            pygame.draw.polygon(
                self.window, globals.main_color, [p.c1, p.c2, p.c3, p.c4]
            )

        # Create next projectile
        self.previous_projectile = self.projectiles.create_next(
            self.previous_projectile, globals.SCREENWIDTH
        )

        # Draw projectiles
        for p in self.projectiles.projectiles:
            pygame.draw.circle(self.window, globals.main_color, (p.x, p.y), p.RADIUS)

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
            self.save_score()
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
            "Lives left: " + str(self.char.lives), True, globals.main_color
        )
        text_lives_left = lives_left.get_rect()
        text_size = globals.font.size("Lives left: " + str(self.char.lives))
        text_lives_left.center = (globals.SCREENWIDTH - int(text_size[0] / 2) - 10, 50)
        self.window.blit(lives_left, text_lives_left)

        time_alive = f"{self.timer.get_time():.4}"
        score = globals.font.render(
            "Time Alive: " + time_alive, True, globals.main_color
        )
        text_score = score.get_rect()
        text_size = globals.font.size("Time Alive: " + time_alive)
        text_score.center = (int(text_size[0] / 2) + 10, 50)
        self.window.blit(score, text_score)

    def save_score(self):
        save_dir = utils.get_save_dir()
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        user = os.getlogin()
        date = datetime.date.today().strftime("%x")
        score = round(self.timer.get_time(), 3)

        assert self.difficulty is not None, "Tried to save score without difficulty"

        savefile = os.path.join(save_dir, "highscores.json")
        if not os.path.exists(savefile):
            scores = {}
            for difficulty in self.difficulty_parameters:
                scores[difficulty] = {}
                for level in self.projectile_types:
                    scores[difficulty][level] = []
            scores[self.difficulty][self.level].append((user, date, score))
        else:
            scores = highscores.get_highscores()
            difficulty_scores = scores.get(self.difficulty, {}).get(self.level, [])
            min_score = (
                min(difficulty_scores, key=lambda x: x[-1])
                if difficulty_scores
                else None
            )
            if len(difficulty_scores) < 5:
                difficulty_scores.append((user, date, score))
            elif min_score and score > min_score[-1]:
                difficulty_scores[-1] = (
                    user,
                    date,
                    score,
                )
            difficulty_scores.sort(key=lambda x: x[-1], reverse=True)

        with open(savefile, "w") as f:
            json.dump(scores, f, indent=4)
