import pygame
import random
from Polygon import Polygon
pygame.init()

SCREENHEIGHT = 480
SCREENWIDTH = 800
WIDTH = 24
HEIGHT = 47
LIVES = 3
LENGTH = 20
JUMP = 10
CHAR_VEL = 10
POLYGON_VEL = 5

x = 0
y = SCREENHEIGHT - HEIGHT
isJump = False
left = False
right = False
walk = 0
lives = LIVES
first_polygon = Polygon((100, SCREENHEIGHT), (100, SCREENHEIGHT - Polygon.length), (100 + Polygon.length, SCREENHEIGHT - Polygon.length), (100 + Polygon.length, SCREENHEIGHT))
first_polygon.add_polygon(first_polygon)
previous_polygon = first_polygon
collided = []
lost_lives = []
clock = pygame.time.Clock()
walk_left = [pygame.image.load("L1.png"), pygame.image.load("L2.png"), pygame.image.load("L3.png"), pygame.image.load("L4.png"), pygame.image.load("L5.png"), pygame.image.load("L6.png"), pygame.image.load("L7.png"), pygame.image.load("L8.png"), pygame.image.load("L9.png")]
walk_right = [pygame.transform.flip(img, True, False) for img in walk_left]
bg = pygame.image.load("bg.jpg")
char = pygame.image.load("standing.png")

w = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("First Game")


font = pygame.font.SysFont("Arial", 32, 1)
game_over = font.render("Game Over! Better luck next time!", True, (255, 0, 0), bg)
text_game_over = game_over.get_rect()
text_game_over.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2))


def draw_char():
    global walk

    if walk + 1 >= 27:
        walk = 0
    if left:
        w.blit(walk_left[walk//3], (x, y))
        walk += 1
    elif right:
        w.blit(walk_right[walk//3], (x, y))
        walk += 1
    else:
        w.blit(char, (x, y))


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

    if keys[pygame.K_a] and x - CHAR_VEL >= 0:
        x -= CHAR_VEL
        left = True
        right = False
        w.blit(char, (x, y))
        pygame.display.update()
    elif keys[pygame.K_d] and x + CHAR_VEL <= SCREENWIDTH - WIDTH:
        x += CHAR_VEL
        left = False
        right = True
        w.blit(char, (x, y))
        pygame.display.update()
    else:
        left = False
        right = False
        walk = 0

    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            left = False
            right = False
            walk = 0
    else:
        if JUMP >= - 10:
            neg = 1
            if JUMP < 0:
                neg = -1
            if y - JUMP >= 0:
                y -= JUMP
                JUMP -= 1
                w.blit(char, (x, y))
                pygame.display.update()
            else:
                JUMP = -JUMP - 1
        else:
            isJump = False
            JUMP = 10

    # Create next polygon
    distance = random.randint(100, 200)
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
        if e.is_collision((x, y + HEIGHT), (x + WIDTH, y + HEIGHT)) and e not in collided:
            collided.append(e)
    pygame.display.update()
    # Decrement lives
    for e in collided:
        if e not in lost_lives and lives - 1 >= 0:
            lives -= 1
            lost_lives.append(e)
        collided.remove(e)

    if lives == 0:
        run = False
    # Move polygons
    for e in Polygon.polygons:
        if e.c1[0] - POLYGON_VEL <= 0:
            e.remove_polygon(e)
        else:
            e.c1 = (e.c1[0] - POLYGON_VEL, e.c1[1])
            e.c2 = (e.c2[0] - POLYGON_VEL, e.c2[1])
            e.c3 = (e.c3[0] - POLYGON_VEL, e.c3[1])
            e.c4 = (e.c4[0] - POLYGON_VEL, e.c4[1])
    
    draw_char()
    draw_life(lives)
    pygame.display.update()

w.blit(game_over, text_game_over)
pygame.display.update()
pygame.time.delay(1000)
pygame.quit()
