import socket,pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.8"
        self.port = 5550
        self.addr = (self.server, self.port)
        network = self.connect()
        self.playerId = network[0]
        self.players = network[1]
        self.coneBlocks = network[2]

    def connect(self):
        try:
            self.client.connect(self.addr)   
            playerIdData = self.client.recv(2048*8)
            playerId = pickle.loads(playerIdData)
            self.client.send(str.encode(f"Received player id = {playerId}"))
            initialPlayers = pickle.loads(self.client.recv(2048*8))
            self.client.send(str.encode(f"Received Players location = {initialPlayers}"))
            coneBlocks = pickle.loads(self.client.recv(2048*8))
            return (playerId,initialPlayers,coneBlocks)
        except socket.error as e:
            print(e)
    
    def send(self,playerPos):
        try:
            # print(f"Send called = {playerPos}")
            self.client.send(pickle.dumps(playerPos))
            self.receivePlayersData()
        except socket.error as e:
            print(e)
    def receivePlayersData(self):
        try:
            playersData = self.client.recv(2048*8)
            players = pickle.loads(playersData)
            # print(f"Receved Players={players}")
            self.players = players
        except socket.error as e:
            print(e)