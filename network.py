import socket
import pickle
from _thread import *
import time

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = "64.227.173.172"
        self.port = 5580
        self.addr = (self.server, self.port)
        # self.p = self.connect()
        network = self.connect()
        self.playerId = network[0] 
        self.players = network[1]
        # self.coneBlocks = network[2]
        self.gameMap = network[2]
        self.goal = network[3]
        self.obstacles = network[4]
        start_new_thread(self.receivePlayersData, ())

    def connect(self):
        try:
            # self.client.connect(self.addr)
            self.client.sendto(str.encode("connection request"), self.addr)
            playerData,add = self.client.recvfrom(4096)
            data = pickle.loads(playerData)
            playerId = data["playerId"]
            gameMap = data["arrMap"]
            initialPlayers = data["players"]
            goal = data["goal"] # goal is a tuple (x,y)
            obstacles = data["obstacles"]
            print("received player id: ", playerId)
            time.sleep(6)
            return playerId, initialPlayers, gameMap , goal,obstacles

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
            playersData,addr = self.client.recvfrom(4096)
            if(playersData is None):
                continue
            data = pickle.loads(playersData)
            if data["type"]=="players":
                self.players = data["players"]
            elif data["type"]=="newScene":
                playerId = data["playerId"]
                gameMap = data["arrMap"]
                initialPlayers = data["players"]
                goal = data["goal"] 
                obstacles = data["obstacles"]
                self.playerId=playerId
                self.gameMap=gameMap
                self.players = initialPlayers
                self.goal = goal
                self.obstacles = obstacles

                

