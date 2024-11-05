import pygame
import globals
import colors


settings_icon = pygame.image.load("images/settings.png")
prev_mode = globals.global_mode


def draw_settings_icon(surface):
    global prev_mode
    settings_width, settings_height = 48, 48

    settings_icon_rect = pygame.Rect(
        (globals.SCREENWIDTH - settings_width - 24, 24),
        (settings_width, settings_height),
    )
    pygame.draw.rect(surface, colors.gray, settings_icon_rect, border_radius=8)

    icon_scale = 0.9
    surface.blit(
        pygame.transform.scale(
            settings_icon,
            (
                icon_scale * settings_icon_rect.width,
                icon_scale * settings_icon_rect.height,
            ),
        ),
        (
            settings_icon_rect.left
            + ((1 - icon_scale) * settings_icon_rect.width) // 2,
            settings_icon_rect.top
            + ((1 - icon_scale) * settings_icon_rect.height) // 2,
        ),
    )
    return settings_icon_rect


def draw_settings_menu(surface):
    menu_width = 0.95 * globals.SCREENWIDTH
    menu_height = 0.95 * globals.SCREENHEIGHT
    menu = pygame.Rect(
        (
            (globals.SCREENWIDTH - menu_width) / 2,
            (globals.SCREENHEIGHT - menu_height) / 2,
        ),
        (menu_width, menu_height),
    )
    pygame.draw.rect(surface, colors.brown, menu, border_radius=24)

    menu_title = globals.font.render("Settings", True, colors.black)
    title_width, title_height = menu_title.get_size()
    surface.blit(
        menu_title,
        (
            (globals.SCREENWIDTH // 2) - (title_width // 2),
            menu.top + (0.05 * menu_height),
        ),
    )

    close_menu_button = pygame.Rect((menu.right - 48 - 24, menu.top + 24), (48, 48))
    pygame.draw.rect(surface, colors.red, close_menu_button, border_radius=8)

    close_menu_text = globals.font.render("X", True, colors.white)
    surface.blit(
        close_menu_text,
        (
            close_menu_button.left
            + ((close_menu_button.width - close_menu_text.get_rect().width) // 2),
            close_menu_button.top
            + ((close_menu_button.height - close_menu_text.get_rect().height) // 2),
        ),
    )

    move_left_text = globals.font.render("Move Left", True, colors.black)
    move_right_text = globals.font.render("Move Right", True, colors.black)
    jump_text = globals.font.render("Jump", True, colors.black)
    action_names = [move_left_text, move_right_text, jump_text]
    row_padding = 24
    col_padding = 24
    col_width = (menu.width - (4 * col_padding)) // 3  # 3 columns, 4 col_paddings
    prev_action_bottom = menu.top + (0.05 * menu_height) + title_height + row_padding
    for action_name in action_names:
        action_name.get_rect().width = col_width
        surface.blit(
            action_name, (menu.left + col_padding, prev_action_bottom + row_padding)
        )

        key1 = pygame.Rect(
            (
                menu.left + col_padding + col_width + col_padding,
                prev_action_bottom + row_padding,
            ),
            (col_width, action_name.get_height()),
        )
        pygame.draw.rect(surface, colors.black, key1, 4, border_radius=8)

        key2 = pygame.Rect(
            (
                menu.left
                + col_padding
                + col_width
                + col_padding
                + col_width
                + col_padding,
                prev_action_bottom + row_padding,
            ),
            (col_width, action_name.get_height()),
        )
        pygame.draw.rect(surface, colors.black, key2, 4, border_radius=8)

        prev_action_bottom += action_name.get_height() + row_padding

    if pygame.event.get(pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.mouse.get_pos()

        if close_menu_button.collidepoint(mouse_pos):
            globals.global_mode = prev_mode
