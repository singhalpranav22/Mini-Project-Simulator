import pygame
import random


class ConeBlock:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.img = pygame.image.load('assets/img.png')
        IMAGE_SMALL = pygame.transform.scale(self.img, (30, 30))
        self.img = IMAGE_SMALL
        if x is None and y is None:
            self.setPosition()

    def setPosition(self):
        self.x = random.randrange(0, 500, 1)
        self.y = random.randrange(0, 500, 1)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))