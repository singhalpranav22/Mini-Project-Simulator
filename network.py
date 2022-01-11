import socket,pickle

class Networkk:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.8"
        self.port = 5556
        self.addr = (self.server, self.port)
        connTuple = self.connect()
        self.playerId = connTuple[0]
        return connTuple

    def getPos(self):
        return self.pos
    def connect(self):
        try:
            self.client.connect(self.addr)   
            playerIdData = self.client.recv(2048)
            playerId = pickle.loads(playerIdData)
            initialPlayers = pickle.load(self.client.recv(2048))
            return (playerId,initialPlayers)
        except socket.error as e:
            print(e)
    
    def send(self,playerPos):
        try:
            self.client.send(pickle.dumps(playerPos))
            return self.receivePlayersData()
        except socket.error as e:
            print(e)
    def receivePlayersData(self):
        try:
            playersData = self.client.recv(2048)
            players = pickle.loads(playersData)
            return players
        except socket.error as e:
            print(e)
