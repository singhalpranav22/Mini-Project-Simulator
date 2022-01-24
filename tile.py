import pygame

class Tile:
    def __init__(self,x,y):
        self.width = 16  
        self.height = 16
        self.x = x 
        self.y = y 
        self.rect = (x, y, self.width, self.height)
        self.color = [150, 75, 0] # brown  
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)