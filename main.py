import pygame
from game import Game
import main_menu
import game_over
import globals
import settings

pygame.init()
pygame.mixer.init()
globals.font = pygame.font.SysFont("Arial", 32, True)

# Window setup
org_w = pygame.display.set_mode((globals.SCREENWIDTH, globals.SCREENHEIGHT))
w = org_w.copy()

# Pygame text setup
pygame.display.set_caption("Jumping Game")

g = Game(w)

while True:
    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        quit()

    match globals.global_mode:
        case "level":
            main_menu.draw_level_menu(org_w, g)
        case "menu":
            main_menu.draw_main_menu(org_w, g)
        case "game":
            g.draw_game()
            org_w.blit(g.window, next(g.offset))
        case "settings":
            settings.draw_settings_menu(org_w)
        case "gameover":
            game_over.draw_game_over(org_w, g)

    pygame.display.update()
