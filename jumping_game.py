import pygame
import random
pygame.init()

w = pygame.display.set_mode((800, 800))

pygame.display.set_caption("First Game")

screenWidth = 800

width = 20
height = 35
radius = 10
x = 0
y = screenWidth - height
v = 5
jump = 5
isJump = False
l = 20

ox = 100
oy = screenWidth
pol = 0
polygons = [(ox, oy), (ox + int(l / 2), oy - l), (ox + l, oy)]

font = pygame.font.Font("freesansbold.ttf", 32)
text = font.render("Game Over! Better luck next time!", True, (255, 0, 0), (0, 0, 0))
text_rect = text.get_rect()
text_rect.center = (int(screenWidth/2), int(screenWidth/2))


def is_overlap():
    result = False
    for i in range(0, len(polygons) - 2, 3):
        if (y + height >= polygons[i+1][1]) and (x + width >= polygons[i][0] and x <= polygons[i+2][0]):
            result = result or True

    return result


run = True
while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and x - v >= 0:
        x = x - v
    if keys[pygame.K_d] and x + v <= screenWidth - width:
        x = x + v
    if not isJump:
        #if keys[pygame.K_w] and y - v >= 0:
            #y = y - v
        #if keys[pygame.K_s] and y + v <= screenWidth - height:
            #y = y + v
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jump >= - 5:
            neg = 1
            if jump < 0:
                neg = -1
            if y - jump - (2 * radius) >= 0:
                y = y - 4 * jump
                jump = jump - 1
            else:
                jump = -jump - 1
        else:
            isJump = False
            jump = 5

    dist = random.randint(50, 100)
    coord1 = (polygons[pol][0] + l + dist, oy)
    coord2 = (coord1[0] + int(l/2), coord1[1] - l)
    coord3 = (coord1[0] + l, coord1[1])
    if coord3[0] <= screenWidth:
        polygons.append(coord1)
        polygons.append(coord2)
        polygons.append(coord3)
        pol += 3

    w.fill((0, 0, 0))
    pygame.draw.rect(w, (255, 0, 0), (x, y, width, height))
    pygame.draw.circle(w, (255, 0, 0), (x + radius, y - radius), radius)
    pygame.display.update()
    for i in range(0, len(polygons) - 2, 3):
        pygame.draw.polygon(w, (255, 0, 0), polygons[i : i + 3])

    pygame.display.update()

    run = not is_overlap()

    for i in range(len(polygons)):
        polygons[i] = (polygons[i][0] - v, polygons[i][1])


w.blit(text, text_rect)
pygame.display.update()
pygame.time.delay(1000)
pygame.quit()
