import globals
import colors
import pygame


def draw_game_over(window, game):
    padding = 20
    center = (globals.SCREENWIDTH // 2, globals.SCREENHEIGHT // 2)

    window.blit(game.bg, (0, 0))

    game_over = globals.font.render(
        f"Game Over! You were alive for {game.timer.get_time():.4} seconds.",
        True,
        colors.red,
    )
    game_over_rect = game_over.get_rect()
    game_over_rect.center = center
    game_over_rect.top = padding
    window.blit(game_over, game_over_rect)

    difficulty = globals.font.render(
        f"High Scores ({game.difficulty})", True, colors.red
    )
    difficulty_rect = difficulty.get_rect()
    difficulty_rect.center = center
    difficulty_rect.top = game_over_rect.bottom + padding
    window.blit(difficulty, difficulty_rect)

    play_again = globals.font.render("Play Again", True, colors.red)
    play_again_rect = play_again.get_rect()
    play_again_rect.center = center
    play_again_rect.bottom = globals.SCREENHEIGHT - padding
    window.blit(play_again, play_again_rect)

    if pygame.event.get(pygame.MOUSEBUTTONUP):
        mouse_pos = pygame.mouse.get_pos()

        if play_again_rect.collidepoint(mouse_pos):
            globals.global_mode = "menu"
