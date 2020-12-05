import pygame
import time
from Polygon import Polygon
from Character import Character
from Utility import Utility
from Projectile import Projectile

pygame.init()

# Window setup
SCREENHEIGHT = 480
SCREENWIDTH = 800
w = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
bg = pygame.image.load("images/bg.jpg")

# Polygon setup
first_polygon = Polygon((100, SCREENHEIGHT), (100, SCREENHEIGHT - Polygon.length), (100 + Polygon.length, SCREENHEIGHT - Polygon.length), (100 + Polygon.length, SCREENHEIGHT))
first_polygon.add_polygon(first_polygon)
previous_polygon = first_polygon
collided_polygons = []
polygon_lost_lives = []

# Character setup
char = Character(0, SCREENHEIGHT - Character.height)
char.make_char()

# Projectile setup
first_projectile = Projectile(SCREENWIDTH-Projectile.radius, SCREENHEIGHT - 2*char.height)
first_projectile.add_projectile(first_projectile)
previous_projectile = first_projectile
collided_projectiles = []
projectile_lost_lives = []

# Pygame text setup
pygame.display.set_caption("First Game")
font = pygame.font.SysFont("Arial", 32, 1)
game_over = font.render("Game Over! Better luck next time!", True, (255, 0, 0), bg)
text_game_over = game_over.get_rect()
text_game_over.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2))

score = 0
clock = pygame.time.Clock()
start = time.time()
run = True

# main
while run:
    clock.tick(30)
    score += 20

    w.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and char.x - char.vel >= 0:
        char.x -= char.vel
        char.left = True
        char.right = False
        w.blit(char.char_img, (char.x, char.y))
        pygame.display.update()
    elif keys[pygame.K_d] and char.x + char.vel <= SCREENWIDTH - char.width:
        char.x += char.vel
        char.left = False
        char.right = True
        w.blit(char.char_img, (char.x, char.y))
        pygame.display.update()
    else:
        char.left = False
        char.right = False
        char.walk = 0

    if not char.isJump:
        if keys[pygame.K_SPACE]:
            char.isJump = True
            char.left = False
            char.right = False
            char.walk = 0
    else:
        if char.jump >= - 10:
            neg = 1
            if char.jump < 0:
                neg = -1
            if char.y - char.jump >= 0:
                char.y -= char.jump
                char.jump -= 1
                w.blit(char.char_img, (char.x, char.y))
                pygame.display.update()
            else:
                char.jump = -char.jump - 1
        else:
            char.isJump = False
            char.jump = 10

    u = Utility()

    # Create next polygon
    previous_polygon = first_polygon.create_next(previous_polygon, SCREENWIDTH)

    # Draw polygons
    u.draw_polygons(first_polygon, char, w, collided_polygons)

    # Create next projectile
    previous_projectile = first_projectile.create_next(previous_projectile, SCREENWIDTH)

    # Draw projectiles
    u.draw_projectiles(first_projectile, char, w, collided_projectiles)

    # Decrement lives

    # Check Polygon collision
    for e in collided_polygons:
        if e not in polygon_lost_lives and char.lives - 1 >= 0:
            char.lives -= 1
            polygon_lost_lives.append(e)
            collided_polygons.remove(e)

    # Check Projectile collision
    for p in collided_projectiles:
        if p not in projectile_lost_lives and char.lives - 1 >= 0:
            char.lives -= 1
            projectile_lost_lives.append(p)
            collided_projectiles.remove(p)

    # Check lives
    if char.lives == 0:
        run = False

    # Move polygons
    first_polygon.move_polygons()

    # Move projectiles
    first_projectile.move_projectiles()

    # Draw character and UI
    u.draw_char(char, w)
    u.draw_life(char.lives, font, w, bg, SCREENWIDTH - 100, 50)
    u.draw_score(score, font, w, bg, 80, 50)
    pygame.display.update()

# Display end screen
end = time.time()
game_over = font.render("Game Over! You were alive for " + str(int(end - start)) + " seconds.", True, (255, 0, 0), bg)
w.blit(game_over, text_game_over)
pygame.display.update()
pygame.time.delay(1000)
pygame.quit()
