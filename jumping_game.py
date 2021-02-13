import pygame
import time
from Polygon import Polygon
from Character import Character
from Utility import Utility
from Projectile import Projectile
from Projectiles import Projectiles
from Polygons import Polygons

pygame.init()
pygame.mixer.init()

# Game variables
SCORE_INCREMENT = 25

# Window setup
SCREENHEIGHT = 480
SCREENWIDTH = 800
main_menu = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
main_menu_bg = pygame.image.load("images/main_menu.png")
w = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
bg = pygame.image.load("images/bg.jpg")

# Pygame text setup
pygame.display.set_caption("First Game")
font = pygame.font.SysFont("Arial", 32, True)

# Main menu setup
difficulty = font.render("Choose your difficulty:", True, (255, 0, 0))
easy = font.render("Easy", True, (255, 0, 0))
medium = font.render("Medium", True, (255, 0, 0))
hard = font.render("Hard", True, (255, 0, 0))
god = font.render("God", True, (255, 0, 0))
text_difficulty = difficulty.get_rect()
text_easy = easy.get_rect()
text_medium = medium.get_rect()
text_hard = hard.get_rect()
text_god = god.get_rect()
text_difficulty.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2) - 70)
text_easy.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2))
text_medium.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2) + 50)
text_hard.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2) + 100)
text_god.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2) + 150)


# main
def main(num_lives, v1=Polygon.VELOCITY, v2=Projectile.VELOCITY):
    # Polygon setup
    Polygon.VELOCITY = v1
    polygons = Polygons()
    first_polygon = Polygon((int(SCREENWIDTH/3), SCREENHEIGHT), (int(SCREENWIDTH/3), SCREENHEIGHT - Polygon.LENGTH), (int(SCREENWIDTH/3) + Polygon.LENGTH, SCREENHEIGHT - Polygon.LENGTH), (int(SCREENWIDTH/3) + Polygon.LENGTH, SCREENHEIGHT))
    polygons.add_polygon(first_polygon)
    previous_polygon = first_polygon
    collided_polygons = []
    polygon_lost_lives = []

    # Projectile setup
    Projectile.VELOCITY = v2
    projectiles = Projectiles()
    first_projectile = Projectile(SCREENWIDTH - Projectile.RADIUS, SCREENHEIGHT - 2 * Character.height)
    projectiles.add_projectile(first_projectile)
    previous_projectile = first_projectile
    collided_projectiles = []
    projectile_lost_lives = []

    # Character setup
    char = Character(0, SCREENHEIGHT - Character.height)
    char.set_lives(num_lives)

    # Game music setup
    if num_lives == 10:
        pygame.mixer.music.load("easy.mp3")
    elif num_lives == 5:
        pygame.mixer.music.load("medium.mp3")
    elif num_lives == 3:
        pygame.mixer.music.load("hard.mp3")
    elif num_lives == 1:
        pygame.mixer.music.load("god.mp3")

    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1, 3)

    score = 0
    clock = pygame.time.Clock()
    start = time.time()
    game_run = True

    while game_run:
        w.blit(bg, (0, 0))
        clock.tick(30)

        char.add_score(SCORE_INCREMENT)

        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                game_run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and char.x - char.vel >= 0:
            char.move_left()
        elif keys[pygame.K_d] and char.x + char.vel <= SCREENWIDTH - char.width:
            char.move_right()
        else:
            char.set_standing()

        if not char.isJump:
            if keys[pygame.K_SPACE]:
                char.set_jump()
        else:
            char.jump()

        u = Utility()

        # Create next polygon
        previous_polygon = polygons.create_next(previous_polygon, SCREENWIDTH)

        # Draw polygons
        u.draw_polygons(polygons, w)

        # Create next projectile
        previous_projectile = projectiles.create_next(previous_projectile, SCREENWIDTH)

        # Draw projectiles
        u.draw_projectiles(projectiles, w)

        # Check Projectile collision
        for p in projectiles.projectiles:
            if p.is_collision(char) and p not in collided_projectiles:
                collided_projectiles.append(p)

        # Check Polygon collision
        for p in polygons.polygons:
            if p.is_collision(char) and p not in collided_polygons:
                collided_polygons.append(p)

        # Decrement lives

        # Check Polygon collision
        for p in collided_polygons:
            if p not in polygon_lost_lives and char.lives - 1 >= 0:
                char.lives -= 1
                polygon_lost_lives.append(p)
                collided_polygons.remove(p)

        # Check Projectile collision
        for p in collided_projectiles:
            if p not in projectile_lost_lives and char.lives - 1 >= 0:
                char.lives -= 1
                projectile_lost_lives.append(p)
                collided_projectiles.remove(p)

        # Check lives
        if char.lives == 0:
            pygame.mixer.music.stop()
            game_run = False

        # Move polygons
        polygons.move_polygons()

        # Move projectiles
        projectiles.move_projectiles()

        # Draw character and UI
        u.draw_char(char, w)
        u.draw_life(char.lives, font, w, SCREENWIDTH)
        u.draw_score(char.score, font, w)
        pygame.display.update()

    # Display end screen
    end = time.time()
    game_over = font.render("Game Over! You were alive for " + str(int(end - start)) + " seconds.", True, (255, 0, 0))
    text_game_over = game_over.get_rect()
    text_game_over.center = (int(SCREENWIDTH/2), int(SCREENHEIGHT/2))
    w.blit(game_over, text_game_over)
    pygame.display.update()
    pygame.time.delay(1000)
    pygame.quit()


main_menu_run = True
lives = 0
projectile_velocity = Projectile.VELOCITY
block_velocity = Polygon.VELOCITY

# Run main menu
while main_menu_run:
    main_menu.blit(main_menu_bg, (0, 0))
    main_menu.blit(difficulty, text_difficulty)
    main_menu.blit(easy, text_easy)
    main_menu.blit(medium, text_medium)
    main_menu.blit(hard, text_hard)
    main_menu.blit(god, text_god)

    for main_menu_event in pygame.event.get():
        if main_menu_event.type == pygame.QUIT:
            main_menu_run = False
        if main_menu_event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if text_easy.collidepoint(mouse_pos):
                lives = 10
                projectile_velocity = int(0.5 * Projectile.VELOCITY)
                block_velocity = int(0.5 * Polygon.VELOCITY)
                main_menu_run = False
            elif text_medium.collidepoint(mouse_pos):
                lives = 5
                projectile_velocity = int(Projectile.VELOCITY)
                block_velocity = int(Polygon.VELOCITY)
                main_menu_run = False
            elif text_hard.collidepoint(mouse_pos):
                lives = 3
                projectile_velocity = int(1.5 * Projectile.VELOCITY)
                block_velocity = int(1.5 * Polygon.VELOCITY)
                main_menu_run = False
            elif text_god.collidepoint(mouse_pos):
                lives = 1
                projectile_velocity = int(2 * Projectile.VELOCITY)
                block_velocity = int(2 * Polygon.VELOCITY)
                main_menu_run = False

    pygame.display.update()

# Run game
main(lives, block_velocity, projectile_velocity)
