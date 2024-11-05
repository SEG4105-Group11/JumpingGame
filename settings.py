import os
import json
import pygame
import globals
import colors
import utils


settings_icon = pygame.image.load("images/settings.png")
prev_mode = globals.global_mode
active_key = (None, None)


data = {
    "Move Left": ["a", "left"],
    "Move Right": ["d", "right"],
    "Jump": ["space", "up"],
}


settings_file = os.path.join(utils.get_save_dir(), "settings.json")
if not os.path.exists(settings_file):
    with open(settings_file, "w") as f:
        json.dump(data, f)
else:
    with open(settings_file, "r") as f:
        data = json.load(f)


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
    global active_key

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

    actions = {
        # action_name: [action_text, key1_rect, key2_rect]
        "Move Left": [globals.font.render("Move Left", True, colors.black), None, None],
        "Move Right": [
            globals.font.render("Move Right", True, colors.black),
            None,
            None,
        ],
        "Jump": [globals.font.render("Jump", True, colors.black), None, None],
    }
    row_padding = 24
    col_padding = 24
    col_width = (menu.width - (4 * col_padding)) // 3  # 3 columns, 4 col_paddings
    prev_action_bottom = menu.top + (0.05 * menu_height) + title_height + row_padding
    for action_name in actions:
        action_text = actions.get(action_name, [])[0]
        action_name_rect = action_text.get_rect()
        action_name_rect.width = col_width
        surface.blit(
            action_text,
            (menu.left + col_padding, prev_action_bottom + row_padding),
        )

        key1_rect = pygame.Rect(
            (
                menu.left + col_padding + col_width + col_padding,
                prev_action_bottom + row_padding,
            ),
            (col_width, action_name_rect.height),
        )
        pygame.draw.rect(
            surface,
            colors.red if active_key == (action_name, 0) else colors.black,
            key1_rect,
            4,
            border_radius=8,
        )
        actions.get(action_name, [])[1] = key1_rect
        key1 = data.get(action_name, [])[0]
        key1_text = globals.font.render(key1, True, colors.black)
        surface.blit(
            key1_text,
            (
                key1_rect.left
                + (key1_rect.right - key1_rect.left - key1_text.get_width()) // 2,
                key1_rect.top,
            ),
        )

        key2_rect = pygame.Rect(
            (
                menu.left
                + col_padding
                + col_width
                + col_padding
                + col_width
                + col_padding,
                prev_action_bottom + row_padding,
            ),
            (col_width, action_name_rect.height),
        )
        pygame.draw.rect(
            surface,
            colors.red if active_key == (action_name, 1) else colors.black,
            key2_rect,
            4,
            border_radius=8,
        )
        actions.get(action_name, [])[2] = key2_rect
        key2 = data.get(action_name, [])[1]
        key2_text = globals.font.render(key2, True, colors.black)
        surface.blit(
            key2_text,
            (
                key2_rect.left
                + (key2_rect.right - key2_rect.left - key2_text.get_width()) // 2,
                key2_rect.top,
            ),
        )

        prev_action_bottom += action_name_rect.height + row_padding

    if pygame.event.get(pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.mouse.get_pos()

        if close_menu_button.collidepoint(mouse_pos):
            globals.global_mode = prev_mode
        else:
            for action_name in actions:
                key1_rect = actions.get(action_name, [])[1]
                key2_rect = actions.get(action_name, [])[2]
                if key1_rect.collidepoint(mouse_pos):
                    active_key = (action_name, 0)
                elif key2_rect.collidepoint(mouse_pos):
                    active_key = (action_name, 1)

    for event in pygame.event.get(pygame.KEYUP):
        key_name = pygame.key.name(event.key)
        active_action_name = active_key[0]
        i = active_key[1]
        if active_action_name is not None and i is not None:
            data[active_action_name][i] = key_name
            with open(settings_file, "w") as f:
                json.dump(data, f)
            active_key = (None, None)
