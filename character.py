import pygame


class Character:
    vel = 10
    jump_count = 10
    lives = 10
    width = 24
    height = 47
    walk_left = [
        pygame.image.load("images/L1.png"),
        pygame.image.load("images/L2.png"),
        pygame.image.load("images/L3.png"),
        pygame.image.load("images/L4.png"),
        pygame.image.load("images/L5.png"),
        pygame.image.load("images/L6.png"),
        pygame.image.load("images/L7.png"),
        pygame.image.load("images/L8.png"),
        pygame.image.load("images/L9.png"),
    ]
    walk_right = [pygame.transform.flip(img, True, False) for img in walk_left]
    char_img = pygame.image.load("images/standing.png")

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.jump_count = Character.jump_count
        self.walk = 0
        self.isJump = False
        self.left = False
        self.right = False
        self.score = 0

    def add_score(self, score):
        self.score += score

    def move_left(self):
        self.x -= self.vel
        self.left = True
        self.right = False

    def move_right(self):
        self.x += self.vel
        self.left = False
        self.right = True

    def set_standing(self):
        self.left = False
        self.right = False
        self.walk = 0

    def set_jump(self):
        self.isJump = True
        self.left = False
        self.right = False
        self.walk = 0

    def jump(self):
        if self.jump_count >= -Character.jump_count:
            neg = 1
            if self.jump_count < 0:
                neg = -1
            if self.jump_count == 0:
                neg = 0
            self.y -= self.jump_count + (0.2 * (self.jump_count**2) * neg)
            self.jump_count -= 1
        else:
            self.isJump = False
            self.jump_count = 10

    def set_lives(self, lives):
        self.lives = lives
