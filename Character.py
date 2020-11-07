import pygame


class Character:
    vel = 10
    jump = 10
    lives = 5
    width = 24
    height = 47
    walk = 0
    x = 0
    y = 0
    w = None
    isJump = False
    left = False
    right = False
    char_img = None
    bg = pygame.image.load("images/bg.jpg")
    walk_left = [pygame.image.load("images/L1.png"), pygame.image.load("images/L2.png"),
                 pygame.image.load("images/L3.png"), pygame.image.load("images/L4.png"),
                 pygame.image.load("images/L5.png"), pygame.image.load("images/L6.png"),
                 pygame.image.load("images/L7.png"), pygame.image.load("images/L8.png"),
                 pygame.image.load("images/L9.png")]

    walk_right = [pygame.transform.flip(img, True, False) for img in walk_left]

    def __init__(self, vel=10, jump=10, lives=5, w=None):
        self.vel = vel
        self.jump = jump
        self.lives = lives
        self.w = w

    def make_char(self):
        self.char_img = pygame.image.load("images/standing.png")

    def draw_char(self):
        if self.walk + 1 >= 27:
            self.walk = 0
        if self.left:
            self.w.blit(self.walk_left[self.walk // 3], (self.x, self.y))
            self.walk += 1
        elif self.right:
            self.w.blit(self.walk_right[self.walk // 3], (self.x, self.y))
            self.walk += 1
        else:
            self.w.blit(self.char_img, (self.x, self.y))
