# the client needs the location of all players for rendering purposes
import pygame ,random
import socket,pickle
from _thread import *
import threading
from network import Network
from cone import ConeBlock

max_speed = 0.4
class Client:
    def __init__(self):
        self.width = self.height = 600
        self.coneBlocks = []
        self.win = pygame.display.set_mode((self.width, self.height))



def redrawWindow(win,players,clientPlayer,client):
    win.fill((255,255,255))
    for cone in client.coneBlocks:
        cone.draw(win)
    for i in range(len(players)):
        if i == clientPlayer.playerId:
            clientPlayer.draw(win)
        else:
            player = players[i]
            pygame.draw.rect(win,player['color'],(player['x'],player['y'],10,10))
    pygame.display.update()




class Player:
    def __init__(self,x,y,width,height,color,client):
        self.client = client
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 1.5
        self.playerId = -1
        self.velX = 0
        self.velY = 0
        self.acceleration = 0.1
        self.friction = 0.99

    def draw (self, win):
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
        
        iscolliding = self.collision()
        if iscolliding == False:
            self.update()
        else:
            self.x -= self.velX
            self.y -= self.velY
            # self.velX /= self.friction
            # self.velY /= self.friction
            self.velX = 0
            self.velY = 0
            self.update()
    
    def collision(self):
        for cone in self.client.coneBlocks:
            if cone.x + cone.width > self.x and cone.x < self.x + self.width:
                if cone.y + cone.height > self.y and cone.y < self.y + self.height:
                    return True
            if self.x<2 or self.y<2 or self.x>self.client.width-10 or self.y>self.client.height-10:
                return True
        return False

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
    


def main():
    run = True 
    # starting the client 
    client = Client()
    network = Network()  
    playerId = network.playerId
    players = network.players
    coneBlocksPos = network.coneBlocks
    for i in range(len(coneBlocksPos)):
        coneBlock = ConeBlock(coneBlocksPos[i][0],coneBlocksPos[i][1])
        client.coneBlocks.append(coneBlock)
    print(client.coneBlocks)
    print(f"Received player id = {playerId}")
    print(f"Received players = {players}")
    pygame.display.set_caption(f"Client:{playerId}")
    clientPlayer = Player(players[playerId]['x'], players[playerId]['y'],10,10,players[playerId]['color'],client)
    clientPlayer.playerId = playerId
    
    redrawWindow(client.win,players,clientPlayer,client)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()
        clientPlayer.move()

        newLocation={"x": clientPlayer.x,"y": clientPlayer.y}
        redrawWindow(client.win,network.players,clientPlayer,client)
        # print(f"New player location={newLocation}")
        # thr = threading.Thread(target=network.send,args=(newLocation,)).start()
        network.send(newLocation)


main()