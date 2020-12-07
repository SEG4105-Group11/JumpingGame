import pygame


class Utility:

    def draw_life(self, num, font, w, screen_width):
        lives_left = font.render("Lives left: " + str(num), True, (255, 0, 0))
        text_lives_left = lives_left.get_rect()
        text_size = font.size("Lives left: " + str(num))
        text_lives_left.center = (screen_width - int(text_size[0] / 2) - 10, 50)
        w.blit(lives_left, text_lives_left)

    def draw_score(self, num, font, w):
        score = font.render("Score: " + str(num), True, (255, 0, 0))
        text_score = score.get_rect()
        text_size = font.size("Score: " + str(num))
        text_score.center = (int(text_size[0] / 2) + 10, 50)
        w.blit(score, text_score)

    def draw_char(self, char, w):
        if char.walk + 1 >= 27:
            char.walk = 0
        if char.left:
            w.blit(char.walk_left[char.walk // 3], (char.x, char.y))
            char.walk += 1
        elif char.right:
            w.blit(char.walk_right[char.walk // 3], (char.x, char.y))
            char.walk += 1
        else:
            w.blit(char.char_img, (char.x, char.y))

    def draw_polygons(self, polygons, w):
        for p in polygons.polygons:
            pygame.draw.polygon(w, (255, 0, 0), [p.c1, p.c2, p.c3, p.c4])

    def draw_projectiles(self, projectiles, w):
        for p in projectiles.projectiles:
            pygame.draw.circle(w, (255, 0, 0), (p.x, p.y), p.RADIUS)
