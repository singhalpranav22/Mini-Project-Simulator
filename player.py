import pygame

max_speed = 0.5


class Player:
    def __init__(self, x, y, width, height, color, client):
        self.client = client
        self.x = x
        self.y = y
        self.goal = (0,0)
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 0.03
        self.playerId = -1
        self.velX = 0
        self.velY = 0
        self.acceleration = 0.03
        self.friction = 0.005

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self, players):
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
        # self.velX *= self.friction
        # self.velY *= self.friction

        isColliding = self.collision(players)
        if isColliding == False:
            self.update()
        else:
            self.x -= self.velX
            self.y -= self.velY
            self.velX = 0
            self.velY = 0
            print(self.x, self.y, self.velX, self.velY)
            self.update()
            print(self.x, self.y, self.velX, self.velY)


    def checkBound(self,x,y):
        if x<0 or y<0 or x>=30 or y>=30:
            return False 
        else:
            return True

    def collision(self, players):
        # For walls
        for i in range(0,30):
            for j in range(0,30):
                if self.client.mapLayout[i][j] == 1:
                    if self.x >= i*16 and self.x <= i*16+16 and self.y >= j*16 and self.y <= j*16+16:
                        return True
                    if self.x +8 >= i*16 and self.x + 8 <= i*16+16 and self.y + 8>= j*16 and self.y +8<= j*16+16:
                        return True
                        
        # For players
        w = self.width
        h = self.height
        for i in range(len(players)):
            if i!=self.playerId:
                x = players[i]['x']
                y = players[i]['y']
                print("Didn't collide yet")
                if (self.x < x + w and self.x + w > x and self.y < y + h and h + self.y > y):
                    print('Collision ho gaya!')
                    return True
                   
        return False
