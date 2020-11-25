import pygame


class Utility:

    def draw_life(self, num, font, w, bg, x, y):
        lives_left = font.render("Lives left: " + str(num), True, (255, 0, 0), bg)
        text_lives_left = lives_left.get_rect()
        text_lives_left.center = (x, y)
        w.blit(lives_left, text_lives_left)

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

    def draw_polygons(self, p, char, w, collided):
        for e in p.polygons:
            pygame.draw.polygon(w, (255, 0, 0), [e.c1, e.c2, e.c3, e.c4])
            if e.is_collision((char.x, char.y + char.height),
                              (char.x + char.width, char.y + char.height)) and e not in collided:
                collided.append(e)
