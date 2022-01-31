import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "20.185.37.144"
        self.port = 5559
        self.addr = (self.server, self.port)
        # self.p = self.connect()
        network = self.connect()
        self.playerId = network[0] 
        self.players = network[1]
        self.coneBlocks = network[2]
        self.gameMap = network[3]

    def connect(self):
        try:
            self.client.connect(self.addr)
            playerIdData = self.client.recv(4096)

            playerId = pickle.loads(playerIdData)
            self.client.send(str.encode(f"Received player id = {playerId}"))
            gameMapData = self.client.recv(4096)
            gameMap = pickle.loads(gameMapData)
            self.client.send(str.encode(f"Received gamemap = {gameMap}"))
            initialPlayers = pickle.loads(self.client.recv(4096))
            self.client.send(str.encode(f"Received Players location = {initialPlayers}"))

            coneBlocks = pickle.loads(self.client.recv(4096))

            return playerId, initialPlayers, coneBlocks, gameMap

        except socket.error as e:
            print(e)

    def send(self, playerPos):
        try:
            self.client.send(pickle.dumps(playerPos))
            self.receivePlayersData()
        except socket.error as e:
            print(e)

    def receivePlayersData(self):
        try:
            playersData = self.client.recv(4096)
            players = pickle.loads(playersData)
            self.players = players
        except socket.error as e:
            print(e)




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

