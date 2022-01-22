import pygame
from network import Network
from cone import ConeBlock
from player import Player

max_speed = 0.4


class Client:
    def __init__(self):
        self.width = self.height = 500
        self.coneBlocks = []
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

def redrawWindow(win, players, clientPlayer, client):
    win.fill((255, 255, 255))
    for cone in client.coneBlocks:
        cone.draw(win)
    for i in range(len(players)):
        if i == clientPlayer.playerId:
            clientPlayer.draw(win)
        else:
            player = players[i]
            pygame.draw.rect(win, player['color'], (player['x'], player['y'], 10, 10))
    pygame.display.update()


def main():
    run = True
    client = Client()
    network = Network()

    playerId = network.playerId
    players = network.players
    coneBlocksPos = network.coneBlocks

    for i in range(len(coneBlocksPos)):
        coneBlock = ConeBlock(coneBlocksPos[i][0], coneBlocksPos[i][1])
        client.coneBlocks.append(coneBlock)

    print(client.coneBlocks)
    # print(f"Received player id = {playerId}")
    # print(f"Received players = {players}")

    pygame.display.set_caption(f"Client:{playerId}")

    clientPlayer = Player(players[playerId]['x'], players[playerId]['y'], 10, 10, players[playerId]['color'], client)
    clientPlayer.playerId = playerId

    redrawWindow(client.win, players, clientPlayer, client)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        clientPlayer.move()

        newLocation = {"x": clientPlayer.x, "y": clientPlayer.y}
        redrawWindow(client.win, network.players, clientPlayer, client)
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