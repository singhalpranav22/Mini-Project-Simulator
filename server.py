import socket
import sys
import pickle
from cone import ConeBlock
from _thread import *
import json
import pygame 
clock = pygame.time.Clock()
import time

class GameState:
    def __init__(self):
        self.numPlayers = -1
        self.playerNetId = {}
        self.players = []  # each element would store the player's location and color
        self.possibleConfig = [([50,50,0], [0, 255, 0]), ([100,100], [255, 0, 0]), ([150, 150], [0, 0, 255]), ([200, 200], [255, 255, 0])]
        self.currConfig = 0
        # blocks
        self.coneBlocks = []
        self.addConeBlocks(0)
        self.arrMap = []
        self.importMapArray()

    def addConeBlocks(self, num=5):
        for i in range(num):
            coneBlock = ConeBlock()
            self.coneBlocks.append((coneBlock.x, coneBlock.y))

    def addNewPlayer(self):
        self.numPlayers += 1
        config = (self.currConfig + 1) % 3
        self.currConfig = config
        self.players.append({'x': self.possibleConfig[config][0][0], 'y': self.possibleConfig[config][0][0], 'color': (self.possibleConfig[config][1][0], self.possibleConfig[config][1][1], self.possibleConfig[config][1][2])})
        return self.numPlayers
    def importMapArray(self):
        f = open('maps.json')
        data = json.load(f)
        self.arrMap = data["map1"]




server = ""
port = 5559

sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)

try:
    sock.bind((server,  port))

except socket.error as msg:
    print("Socket creation error: " + str(msg))
    sys.exit()

print(f"UDP server Listening on {server}: {port}")

game = GameState()  # initialisation of game


# def threaded_client(conn, playerId):
#     toSendId = pickle.dumps(playerId)
#     conn.send(toSendId)
#     confirmation = conn.recv(4096).decode('utf-8')
#     print(confirmation)
#     print(game.arrMap)
#     toSendMap = pickle.dumps(game.arrMap)
#     conn.send(toSendMap)
#     confirmation = conn.recv(4096).decode('utf-8')
#     print(confirmation)
#     intialPlayers = game.players
#     conn.send(pickle.dumps(intialPlayers))
#     print(game.players)
#     confirmation = conn.recv(4096).decode('utf-8')
#     print(confirmation)
#     conn.send(pickle.dumps(game.coneBlocks))

#     # client would send its position continuously
#     while True:
#         # time.sleep(0.1)
#         try:
#             playerLocationData = conn.recv(4096)
#             playerLocation = pickle.loads(playerLocationData)
#             if playerLocation is None:
#                 print('No data recv!')
#                 continue
#             # print(f'New Player location received from id = {playerId} is player:{ playerLocation}')
#             game.players[playerId]['x'] = playerLocation['x']
#             game.players[playerId]['y'] = playerLocation['y']
#             replyData = pickle.dumps(game.players)  # reply sent containing location of all players
#             conn.send(replyData)
#         except socket.timeout:
#             print("Timeout")
#     print(f"Connection Closed, player id : {playerId}")
#     conn.close()


def sendLocationsToPlayers():
    while True:
        time.sleep(0.02)
        playersLocation = pickle.dumps(game.players)
        for dic in game.playerNetId:
            # print(dic)
            sock.sendto(playersLocation, dic)
            
start_new_thread(sendLocationsToPlayers, ())
def newPlayer(addr,sock):
    playerId = game.addNewPlayer()
    game.playerNetId[addr] = {"playerId": playerId,"addr":addr}
    toSend = {
        "playerId": playerId,
        "arrMap": game.arrMap,
        "players": game.players,
    }
    sock.sendto(pickle.dumps(toSend),addr)
    # sock.sendto(pickle.dumps(game.arrMap),addr)
    # sock.sendto(pickle.dumps(game.players),addr)

while True:
    # conn, addr = s.accept()
    # print(f"Connected to: {addr}")
    message,addr = sock.recvfrom(2048)
    if(addr is None):
        continue
    if(addr not in game.playerNetId):
        start_new_thread(newPlayer, (addr,sock))
        # start_new_thread(threaded_client, (sock, playerId))
    else:
        playerId = game.playerNetId[addr]["playerId"]
        playerLocation = pickle.loads(message)
        if playerLocation is None:
                print('No data recv!')
                continue
            # print(f'New Player location received from id = {playerId} is player:{ playerLocation}')
        game.players[playerId]['x'] = playerLocation['x']
        game.players[playerId]['y'] = playerLocation['y']




    # playerId = game.addNewPlayer()
    # print(game.players)
    # start_new_thread(threaded_client, (conn, playerId, ))


