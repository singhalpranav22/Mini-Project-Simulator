import pygame,time
from network import Network
from cone import ConeBlock
from player import Player
from tile import Tile
from _thread import *

max_speed = 0.5

FPS=60
clock = pygame.time.Clock()
class Client:
    def __init__(self):
        self.width = self.height = 480
        self.coneBlocks = []
        self.mapLayout = []
        self.players = []
        self.win = pygame.display.set_mode((self.width, self.height))

# width = 600
# height = 600
# win = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Client")

# def redrawWindowOld(win, player, player2):
#     win.fill((255, 255, 255))
#     player.draw(win)
#     player2.draw(win)
#     pygame.display.update()

def redrawWindow(win, players, clientPlayer,gameMap, client):
    win.fill((255,248,231)) 
    for i in range(0,480,16):
        for j in range(0,480,16):
            if gameMap[i//16][j//16] == 1:
                tile = Tile(i,j)
                tile.draw(win)
            else:
                pass
    # for cone in client.coneBlocks:
    #     cone.draw(win)
    for i in range(len(players)):
        if i == clientPlayer.playerId:
            clientPlayer.draw(win)
        else:
            player = players[i]
            pygame.draw.rect(win, player['color'], (player['x'], player['y'], 8, 8))
    pygame.display.update()


def main():
    run = True
    client = Client()
    network = Network()

    playerId = network.playerId
    players = network.players
    print(players)
    # coneBlocksPos = network.coneBlocks
    gameMap = network.gameMap
    print(gameMap)

    # for i in range(len(coneBlocksPos)):
    #     coneBlock = ConeBlock(coneBlocksPos[i][0], coneBlocksPos[i][1])
    #     client.coneBlocks.append(coneBlock)

    # print(client.coneBlocks)

    client.mapLayout = gameMap
    # print(f"Received player id = {playerId}")
    # print(f"Received players = {players}")

    pygame.display.set_caption(f"Client:{playerId}")

    clientPlayer = Player(players[playerId]['x'], players[playerId]['y'], 8, 8, players[playerId]['color'], client)
    clientPlayer.playerId = playerId

    redrawWindow(client.win, players, clientPlayer, gameMap, client)
    start_new_thread(sendPlayerData, (network, clientPlayer))
    while run:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        client.players = players
        clientPlayer.move(client.players)

        newLocation = {"x": clientPlayer.x, "y": clientPlayer.y}

        redrawWindow(client.win, network.players, clientPlayer, gameMap,client)
        network.send(newLocation)


def sendPlayerData(network,clientPlayer):
    while True:
        time.sleep(0.01)
        # print("Sending player data")
        # print(client.players)
        newLocation = {"x": clientPlayer.x, "y": clientPlayer.y}
        network.send(newLocation)

main()

# def mainOld():
#     run = True
#     n = Network()
#     p = n.getP()
#     clock = pygame.time.Clock()
#
#     while run:
#         clock.tick(60)
#         p2 = n.send(p)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#
#         p.move()
#         redrawWindow(win, p, p2)