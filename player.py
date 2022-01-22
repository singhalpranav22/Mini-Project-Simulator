import pygame

max_speed = 1


class Player:
    def __init__(self, x, y, width, height, color, client):
        self.client = client
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 0.5
        self.playerId = -1
        self.velX = 0
        self.velY = 0
        self.acceleration = 0.1
        self.friction = 0.99

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
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

        isColliding = self.collision()
        if not isColliding:
            self.update()
        else:
            self.x -= self.velX
            self.y -= self.velY
            self.velX = 0
            self.velY = 0
            self.update()

    def collision(self):
        for cone in self.client.coneBlocks:
            if cone.x + cone.width > self.x and cone.x < self.x + self.width:
                if cone.y + cone.height > self.y and cone.y < self.y + self.height:
                    return True
            if self.x < 2 or self.y < 2 or self.x > self.client.width - 10 or self.y > self.client.height - 10:
                return True
        return False

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
