import pygame

max_speed = 0.1


class Player:
    def __init__(self, x, y, width, height, color, client):
        self.client = client
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 0.03
        self.playerId = -1
        self.velX = 0
        self.velY = 0
        self.acceleration = 0.1
        self.friction = 0.99

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self,players):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.velX > -max_speed:
                self.velX -= self.acceleration

        if keys[pygame.K_RIGHT]:
            if self.velX < max_speed:
                self.velX += self.acceleration

        if keys[pygame.K_UP]:
            if self.velY > -max_speed:
                self.velY -= self.acceleration

        if keys[pygame.K_DOWN]:
            if self.velY < max_speed:
                self.velY += self.acceleration

        self.x += self.velX
        self.y += self.velY
        self.velX *= self.friction
        self.velY *= self.friction

        isColliding = self.collision(players)
        if not isColliding:
            self.update()
        else:
            self.x -= self.velX
            self.y -= self.velY
            self.velX = 0
            self.velY = 0
            self.update()

    def checkBound(self,x,y):
        if x<0 or y<0 or x>=30 or y>=30:
            return False 
        else:
            return True

    def collision(self,players):
        # for i in range(0, 30):
        #     for j in range(0, 30):
        #         if 
        # xNearest = (int)((self.x//16)*16) 
        # yNearest = (int)((self.y//16)*16)
        # x = xNearest//16
        # y = yNearest//16
        # if(self.client.mapLayout[x][y] == 1):
        #     return True
        # if(self.checkBound(x+1,y) and self.client.mapLayout[x+1][y] == 1):
        #     return True 
        # if(self.checkBound(x-1,y) and self.client.mapLayout[x-1][y] == 1):
        #     return True
        # if(self.checkBound(x,y+1) and self.client.mapLayout[x][y+1] == 1):
        #     return True
        # if(self.checkBound(x,y-1) and self.client.mapLayout[x][y-1] == 1):
        #     return True
        # if(self.checkBound(x+1,y+1) and self.client.mapLayout[x+1][y+1] == 1):
        #     return True
        # return False
        for i in range(0,30):
            for j in range(0,30):
                if self.client.mapLayout[i][j] == 1:
                    if self.x >= i*16 and self.x <= i*16+16 and self.y >= j*16 and self.y <= j*16+16:
                        return True
                    if self.x +8 >= i*16 and self.x + 8 <= i*16+16 and self.y + 8>= j*16 and self.y +8<= j*16+16:
                        return True
        # for i in range(len(players)):
        #     if i != self.playerId:
        #         if self.x >= players[i]['x'] or self.x <= players[i]['x']+8 or self.y >= players[i]['y'] or self.y <= players[i]['y']+8:
        #             return True
        #         if self.x +8 >= players[i]['x'] or self.x + 8 <= players[i]['x'] or self.y + 8>= players[i]['y'] or self.y +8<= players[i]['y']+8:
        #             return True
        # return False

        # for cone in self.client.coneBlocks:
        #     if cone.x + cone.width > self.x and cone.x < self.x + self.width:
        #         if cone.y + cone.height > self.y and cone.y < self.y + self.height:
        #             return True
        #     if self.x < 2 or self.y < 2 or self.x > self.client.width - 10 or self.y > self.client.height - 10:
        #         return True
        # return False

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
