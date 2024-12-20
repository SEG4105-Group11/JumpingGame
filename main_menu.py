import pygame
import globals
import colors
import settings
from character import Character
from projectile import Projectile


main_menu_bg = pygame.image.load("images/main_menu.png")
back_btn_img = pygame.image.load("images/back-button.png")


def draw_level_menu(window, game):
    padding = 20

    level = globals.font.render(
        "Choose the level you want to play: ", True, colors.black
    )
    level_rect = level.get_rect()
    l1 = globals.font.render("Night Stars", True, colors.black)
    l1_rect = l1.get_rect()
    l2 = globals.font.render("Pixel Monsters", True, colors.black)
    l2_rect = l2.get_rect()
    l3 = globals.font.render("Scary Wolf", True, colors.black)
    l3_rect = l3.get_rect()

    level_rects = [(level, level_rect), (l1, l1_rect), (l2, l2_rect), (l3, l3_rect)]

    rects_height = sum([rect.height for (_, rect) in level_rects]) + (
        (len(level_rects) - 1) * padding
    )

    window.blit(main_menu_bg, (0, 0))

    settings_icon_rect = settings.draw_settings_icon(window)

    y = (globals.SCREENHEIGHT - rects_height) // 2
    x = globals.SCREENWIDTH // 2
    for text, rect in level_rects:
        rect.center = (x, y + padding + (rect.height // 2))
        y = rect.bottom
        window.blit(text, rect)

    if pygame.event.get(pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.mouse.get_pos()

        if settings_icon_rect.collidepoint(mouse_pos):
            settings.prev_mode = globals.global_mode
            globals.global_mode = "settings"
        elif l1_rect.collidepoint(mouse_pos):
            game.level = "Night Stars"
            game.bg = pygame.image.load("images/level_1_bg.png")
            globals.main_color = colors.yellow
        elif l2_rect.collidepoint(mouse_pos):
            game.level = "Pixel Monsters"
            game.bg = pygame.image.load("images/level_2_bg.png")
            globals.main_color = colors.pink
            Projectile.SIN_AMPLITUDE = Character.height
        elif l3_rect.collidepoint(mouse_pos):
            game.level = "Scary Wolf"
            game.bg = pygame.image.load("images/level_3_bg.png")
            globals.main_color = colors.red
            Projectile.SIN_AMPLITUDE = 2 * Character.height
            Projectile.SIN_FREQ = 0.5

        if game.level:
            globals.global_mode = "menu"


def draw_main_menu(window, game):
    padding = 20

    difficulty = globals.font.render(
        "Choose your difficulty:", True, globals.main_color
    )
    difficulty_rect = difficulty.get_rect()
    easy = globals.font.render("Easy", True, globals.main_color)
    easy_rect = easy.get_rect()
    medium = globals.font.render("Medium", True, globals.main_color)
    medium_rect = medium.get_rect()
    hard = globals.font.render("Hard", True, globals.main_color)
    hard_rect = hard.get_rect()
    god = globals.font.render("God", True, globals.main_color)
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

    window.blit(game.bg, (0, 0))

    back_btn_width, back_btn__height = 48, 48
    back_btn_rect = pygame.Rect(
        (24, 24),
        (back_btn_width, back_btn__height),
    )
    pygame.draw.rect(window, colors.gray, back_btn_rect, border_radius=8)

    icon_scale = 0.9
    window.blit(
        pygame.transform.scale(
            back_btn_img,
            (
                icon_scale * back_btn_rect.width,
                icon_scale * back_btn_rect.height,
            ),
        ),
        (
            back_btn_rect.left + ((1 - icon_scale) * back_btn_rect.width) // 2,
            back_btn_rect.top + ((1 - icon_scale) * back_btn_rect.height) // 2,
        ),
    )

    settings_icon_rect = settings.draw_settings_icon(window)

    y = (globals.SCREENHEIGHT - rects_height) // 2
    x = globals.SCREENWIDTH // 2
    for text, rect in text_rects:
        rect.center = (x, y + padding + (rect.height // 2))
        y = rect.bottom
        window.blit(text, rect)

    if pygame.event.get(pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.mouse.get_pos()

        if settings_icon_rect.collidepoint(mouse_pos):
            settings.prev_mode = globals.global_mode
            globals.global_mode = "settings"
        elif back_btn_rect.collidepoint(mouse_pos):
            globals.global_mode = "level"
        elif easy_rect.collidepoint(mouse_pos):
            game.difficulty = "Easy"
        elif medium_rect.collidepoint(mouse_pos):
            game.difficulty = "Medium"
        elif hard_rect.collidepoint(mouse_pos):
            game.difficulty = "Hard"
        elif god_rect.collidepoint(mouse_pos):
            game.difficulty = "God"

        if game.difficulty:
            globals.global_mode = "game"
            game.initialize()
