import pygame


class Character:
    vel = 10
    jump = 10
    lives = 5
    width = 24
    height = 47
    walk = 0
    char_img = None
    walk_left = [pygame.image.load("images/L1.png"), pygame.image.load("images/L2.png"),
                 pygame.image.load("images/L3.png"), pygame.image.load("images/L4.png"),
                 pygame.image.load("images/L5.png"), pygame.image.load("images/L6.png"),
                 pygame.image.load("images/L7.png"), pygame.image.load("images/L8.png"),
                 pygame.image.load("images/L9.png")]
    walk_right = [pygame.transform.flip(img, True, False) for img in walk_left]

    def __init__(self, x=0, y=0, jump=10, walk=0, isJump=False, left=False, right=False):
        self.x = x
        self.y = y
        self.jump = jump
        self.walk = walk
        self.isJump = isJump
        self.left = left
        self.right = right

    def make_char(self):
        self.char_img = pygame.image.load("images/standing.png")

