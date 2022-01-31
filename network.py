import socket
import pickle
from _thread import *
import time
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = "192.168.1.8"
        self.port = 5559
        self.addr = (self.server, self.port)
        # self.p = self.connect()
        network = self.connect()
        self.playerId = network[0] 
        self.players = network[1]
        # self.coneBlocks = network[2]
        self.gameMap = network[2]
        start_new_thread(self.receivePlayersData, ())

    def connect(self):
        try:
            # self.client.connect(self.addr)
            self.client.sendto(str.encode("connection request"), self.addr)
            time.sleep(0.2)
            playerIdData = self.client.recv(4096)
            playerId = pickle.loads(playerIdData)
            # self.client.send(str.encode(f"Received player id = {playerId}"))
            time.sleep(0.2)
            gameMapData = self.client.recv(4096)
            gameMap = pickle.loads(gameMapData)
            # self.client.send(str.encode(f"Received gamemap = {gameMap}"))
            time.sleep(0.2)
            initialPlayers = pickle.loads(self.client.recv(4096))
            # self.client.send(str.encode(f"Received Players location = {initialPlayers}"))

            # coneBlocks = pickle.loads(self.client.recv(4096))

            return playerId, initialPlayers, gameMap

        except socket.error as e:
            print(e)

    def send(self, playerPos):
        try:
            self.client.sendto(pickle.dumps(playerPos), self.addr)
            # self.receivePlayersData()
        except socket.error as e:
            print(e)

    def receivePlayersData(self):
        while True:
            time.sleep(0.01)
            playersData,addr = self.client.recvfrom(4096)
            if(playersData is None):
                continue
            players = pickle.loads(playersData)
            self.players = players
       




    # def getP(self):
    #     return self.p
    #
    # def connect(self):
    #     try:
    #         self.client.connect(self.addr)
    #         return pickle.loads(self.client.recv(4096))
    #     except:
    #         pass
    #
    # def send(self, data):
    #     try:
    #         self.client.send(pickle.dumps(data))
    #         return pickle.loads(self.client.recv(4096))
    #     except socket.error as e:
    #         print(e)

