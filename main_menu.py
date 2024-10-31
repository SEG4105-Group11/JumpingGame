import pygame
import globals
import colors


main_menu_bg = pygame.image.load("images/main_menu.png")

def draw_level_menu(window, game):
    padding = 20

    level = globals.font.render("Choose the level you want to play: ", True, colors.red)
    level_rect = level.get_rect()
    l1 = globals.font.render("<Name of level 1>", True, colors.red)
    l1_rect = l1.get_rect()
    l2 = globals.font.render("<Name of level 2>", True, colors.red)
    l2_rect = l2.get_rect()
    l3 = globals.font.render("<Name of level 3>", True, colors.red)
    l3_rect = l3.get_rect()

    level_rects = [
        (level, level_rect),
        (l1, l1_rect),
        (l2, l2_rect),
        (l3, l3_rect)
    ]

    rects_height = sum([rect.height for (_, rect) in level_rects]) + (
        (len(level_rects) - 1) * padding
    )

    window.blit(main_menu_bg, (0, 0))

    y = (globals.SCREENHEIGHT - rects_height) // 2
    x = globals.SCREENWIDTH // 2
    for text, rect in level_rects:
        rect.center = (x, y + padding + (rect.height // 2))
        y = rect.bottom
        window.blit(text, rect)

    if pygame.event.get(pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.mouse.get_pos()

        if l1_rect.collidepoint(mouse_pos):
            game.__level = "l1"
        elif l2_rect.collidepoint(mouse_pos):
            game.__level = "l2"
        elif l3_rect.collidepoint(mouse_pos):
            game.__level = "l3"

        if game.__level:
            globals.global_mode = "menu"

def draw_main_menu(window, game):
    padding = 20

    difficulty = globals.font.render("Choose your difficulty:", True, colors.red)
    difficulty_rect = difficulty.get_rect()
    easy = globals.font.render("Easy", True, colors.red)
    easy_rect = easy.get_rect()
    medium = globals.font.render("Medium", True, colors.red)
    medium_rect = medium.get_rect()
    hard = globals.font.render("Hard", True, colors.red)
    hard_rect = hard.get_rect()
    god = globals.font.render("God", True, colors.red)
    god_rect = god.get_rect()

    text_rects = [
        (difficulty, difficulty_rect),
        (easy, easy_rect),
        (medium, medium_rect),
        (hard, hard_rect),
        (god, god_rect),
    ]
    rects_height = sum([rect.height for (_, rect) in text_rects]) + (
        (len(text_rects) - 1) * padding
    )

    window.blit(main_menu_bg, (0, 0))

    y = (globals.SCREENHEIGHT - rects_height) // 2
    x = globals.SCREENWIDTH // 2
    for text, rect in text_rects:
        rect.center = (x, y + padding + (rect.height // 2))
        y = rect.bottom
        window.blit(text, rect)

    if pygame.event.get(pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.mouse.get_pos()

        if easy_rect.collidepoint(mouse_pos):
            game.difficulty = "easy"
        elif medium_rect.collidepoint(mouse_pos):
            game.difficulty = "medium"
        elif hard_rect.collidepoint(mouse_pos):
            game.difficulty = "hard"
        elif god_rect.collidepoint(mouse_pos):
            game.difficulty = "god"

        if game.difficulty:
            globals.global_mode = "game"
            game.initialize()
