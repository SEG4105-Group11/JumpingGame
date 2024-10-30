import globals
import colors


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
