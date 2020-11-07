import pygame
import random
from Polygon import Polygon
from Character import Character
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
collided = []
lost_lives = []
clock = pygame.time.Clock()

# Character setup
char = Character(10, 10, 5, w)
char.make_char()
char.x = 0
char.y = SCREENHEIGHT - char.height

# Pygame text setup
pygame.display.set_caption("First Game")
font = pygame.font.SysFont("Arial", 32, 1)
game_over = font.render("Game Over! Better luck next time!", True, (255, 0, 0), bg)
text_game_over = game_over.get_rect()
text_game_over.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2))


def draw_life(num):
    lives_left = font.render("Lives left: " + str(num), True, (255, 0, 0), bg)
    text_lives_left = lives_left.get_rect()
    text_lives_left.center = (SCREENWIDTH - 100, 50)
    w.blit(lives_left, text_lives_left)


run = True
# main
while run:
    clock.tick(27)
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
        walk = 0

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

    # Create next polygon
    distance = random.randint(200, 300)
    coord1 = (previous_polygon.c1[0] + distance, previous_polygon.c1[1])
    coord2 = (previous_polygon.c2[0] + distance, previous_polygon.c2[1])
    coord3 = (previous_polygon.c3[0] + distance, previous_polygon.c3[1])
    coord4 = (previous_polygon.c4[0] + distance, previous_polygon.c4[1])
    if coord4[0] <= SCREENWIDTH:
        next_polygon = Polygon(coord1, coord2, coord3, coord4)
        next_polygon.add_polygon(next_polygon)
        previous_polygon = next_polygon

    w.blit(bg, (0, 0))

    # Draw polygons
    for e in Polygon.polygons:
        pygame.draw.polygon(w, (255, 0, 0), [e.c1, e.c2, e.c3, e.c4])
        if e.is_collision((char.x, char.y + char.height), (char.x + char.width, char.y + char.height)) and e not in collided:
            collided.append(e)
    pygame.display.update()
    # Decrement lives
    for e in collided:
        if e not in lost_lives and char.lives - 1 >= 0:
            char.lives -= 1
            lost_lives.append(e)
        collided.remove(e)
    # Check lives
    if char.lives == 0:
        run = False
    # Move polygons
    for e in Polygon.polygons:
        if e.offscreen:
            e.remove_polygon(e)
        else:
            e.c1 = (e.c1[0] - Polygon.vel, e.c1[1])
            e.c2 = (e.c2[0] - Polygon.vel, e.c2[1])
            e.c3 = (e.c3[0] - Polygon.vel, e.c3[1])
            e.c4 = (e.c4[0] - Polygon.vel, e.c4[1])

    char.draw_char()
    draw_life(char.lives)
    pygame.display.update()

w.blit(game_over, text_game_over)
pygame.display.update()
pygame.time.delay(1000)
pygame.quit()
