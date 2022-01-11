# the client needs the location of all players for rendering purposes
import pygame 
import socket,pickle
from _thread import *
import threading
class Networkk:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.8"
        self.port = 5554
        self.addr = (self.server, self.port)
        connTuple = self.connect()
        self.playerId = connTuple[0]
        self.players = connTuple[1]

    def getPos(self):
        return self.pos
    def connect(self):
        try:
            self.client.connect(self.addr)   
            playerIdData = self.client.recv(2048*8)
            playerId = pickle.loads(playerIdData)
            self.client.send(str.encode(f"Received player id = {playerId}"))
            initialPlayers = pickle.loads(self.client.recv(2048*8))
            return (playerId,initialPlayers)
        except socket.error as e:
            print(e)
    
    def send(self,playerPos):
        try:
            print(f"Send called = {playerPos}")
            self.client.send(pickle.dumps(playerPos))
            self.receivePlayersData()
        except socket.error as e:
            print(e)
    def receivePlayersData(self):
        try:
            playersData = self.client.recv(2048*8)
            players = pickle.loads(playersData)
            print(f"Receved Players={players}")
            self.players = players
        except socket.error as e:
            print(e)

width = height = 500
win = pygame.display.set_mode((width, height))



def redrawWindow(win,players,clientPlayer):
    win.fill((255,255,255))
    for i in range(len(players)):
        if i == clientPlayer.playerId:
            clientPlayer.draw()
        else:
            player = players[i]
            pygame.draw.rect(win,player['color'],(player['x'],player['y'],10,10))
    pygame.display.update()


class Player:
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 1.5
        self.playerId = -1
    def draw(self):
        pygame.draw.rect(win,self.color,self.rect)
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        
        if keys[pygame.K_UP]:
            self.y -= self.vel
        
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.rect = (self.x,self.y,self.width,self.height)
    


def main():
    run = True 
    # starting the client 
    connTuple = Networkk()  
    playerId = connTuple.playerId
    players = connTuple.players
    print(f"Received player id = {playerId}")
    print(f"Received players = {players}")
    pygame.display.set_caption(f"Client:{playerId}")
    clientPlayer = Player(players[playerId]['x'], players[playerId]['y'],10,10,players[playerId]['color'])
    clientPlayer.playerId = playerId
    redrawWindow(win,players,clientPlayer)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()
        clientPlayer.move()
        newLocation={"x": clientPlayer.x,"y": clientPlayer.y}
        redrawWindow(win,connTuple.players,clientPlayer)
        print(f"New player location={newLocation}")
        # thr = threading.Thread(target=connTuple.send,args=(newLocation,)).start()
        connTuple.send(newLocation)


main()