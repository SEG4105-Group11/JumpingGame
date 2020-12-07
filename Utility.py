import pygame


class Utility:

    def draw_life(self, num, font, w, bg, x, y):
        lives_left = font.render("Lives left: " + str(num), True, (255, 0, 0), bg)
        text_lives_left = lives_left.get_rect()
        text_lives_left.center = (x, y)
        w.blit(lives_left, text_lives_left)

    def draw_score(self, num, font, w, bg, x, y):
        score = font.render("Score: " + str(num), True, (255, 0, 0), bg)
        text_score = score.get_rect()
        text_score.center = (x, y)
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
