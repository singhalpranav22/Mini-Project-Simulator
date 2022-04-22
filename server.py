import socket
import sys
import pickle
from _thread import *
import json
import pygame 
clock = pygame.time.Clock()
import time
import random
import csv
import numpy as np
from numpy.linalg import norm
class GameState:
    def __init__(self):
        self.numPlayers = -1
        self.playerNetId = {}
        self.players = []  # each element would store the player's location and color
        self.possibleConfig = [([50,50], [0, 0, 102]), ([100,100], [255, 0, 0]), ([150, 150], [0, 0, 255]), ([200, 200], [0, 204, 204]), ([150, 200], [0, 255, 255]), ([100, 300], [102, 0, 204]),([400,400], [0, 0, 102]),([350,350], [0, 0, 102]),([280,280], [0, 0, 102])]
        # group 1
        center1 = (random.randint(10,460), random.randint(10,460))
        x1 = center1[0]
        y1 = center1[1]
        self.possibleConfig1 = [(x1-14,y1),(x1-4,y1),(x1+6,y1),(x1-4,y1-14),(x1-4,y1+9)]
        # group 2
        center2 = (random.randint(10,460), random.randint(10,460))
        x2 = center2[0]
        y2 = center2[1]
        self.possibleConfig2 = [(x2-14,y2),(x2-4,y2),(x2+6,y2),(x2-4,y2-14),(x2-4,y2+9)]
        self.currConfig = 0
        self.arrMap = []
        self.importMapArray()
        self.goal1 = (random.randint(10,460), random.randint(10,460))
        self.goal2 = (random.randint(10,460), random.randint(10,460))

    def addNewPlayer(self):
        # two groups
        # first group - red (0-4)
        # second group - blue (5-8)

        self.numPlayers += 1
        goal = None
        if self.numPlayers<=4:
            config = (self.currConfig + 1) % 10
            self.currConfig = config
            self.players.append({'x': self.possibleConfig1[self.numPlayers][0], 'y': self.possibleConfig1[self.numPlayers][1], 'color': (255,0,0), "goal": self.goal1})
            goal = self.goal1
        else:
            config = (self.currConfig + 1) % 10
            self.currConfig = config
            self.players.append({'x': self.possibleConfig2[self.numPlayers%5][0], 'y': self.possibleConfig2[self.numPlayers%5][1], 'color': (0,0,255), "goal": self.goal2})
            goal = self.goal2
        return self.numPlayers,goal
    
    def importMapArray(self):
        f = open('maps.json')
        data = json.load(f)
        self.arrMap = data["map2"]

  
       
server = ""
port = 5580

sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)

try:
    sock.bind((server,  port))

except socket.error as msg:
    print("Socket creation error: " + str(msg))
    sys.exit()

print(f"UDP server Listening on {server}: {port}")

game = GameState()  # initialisation of game


def sendLocationsToPlayers():
    while True:
        time.sleep(0.04)
        data = {}
        data["type"] = "players"
        data["players"] = game.players
        playersLocation = pickle.dumps(data)
        for dic in game.playerNetId:
            sock.sendto(playersLocation, dic)
            
start_new_thread(sendLocationsToPlayers, ())

hasStarted = False
def recordData():
    while True:
        inp = input("Enter 'yes' to start the game! =  ")
        if inp != "yes":
            print("Ending game!!")
            break
        sceneNumber = input('Enter the scene number(like 1,2,23,....) : ')
        frameNumbers = int(input('Number of frames to record : '))
        numObstacles = int(input('Number of obstacles : '))
        obstacleList = []
        for i in range(numObstacles):
            print(f"For obstacle {i+1}:")
            x = int(input('Enter x coordinate : '))
            y = int(input('Enter y coordinate : '))
            obstacleList.append({"x":x,"y":y})
        game.numPlayers=-1
        game.players = []
        for dic in game.playerNetId:
            data = {}
            data["type"] = "newScene"
            playerId, goal = game.addNewPlayer()
            data = {
            "type" : "newScene",
            "playerId": playerId,
            "arrMap": game.arrMap,
            "players": game.players,
            "goal": goal,
            "obstacles" : obstacleList, 
            }

            sock.sendto(pickle.dumps(data), dic)
        groups = {}
        groupNum = int(input('Enter number of groups : '))
        for i in range(groupNum):
            print(f'Enter group {i+1} members = ',end="")
            lst = input().split(' ')
            groups[i+1] = lst
        print('Start again ? (Y/N) = ',end="")
        inp = input()
        if(inp=="Y" or inp=="y"):
            continue
        print("Game starting in 5 seconds........")
        print('Data recording has been started')
        data = []
        curr = 0
        fields = ['frameNumber','1','2','3','4','5','6']
        while curr<=frameNumbers:
            curr+=1
            time.sleep(0.25)
            players = game.players
            arr = [curr,-1,-1,-1,-1,-1,-1]
            for i in range(len(players)):
                arr[i+1] = players[i]['x']
            data.append(arr)
            arr = [curr,-1,-1,-1,-1,-1,-1]
            for i in range(len(players)):
                arr[i+1] = players[i]['y']
            data.append(arr)

            
        filename = f"scenes/scene/scene{sceneNumber}.csv"
        
    # writing to csv file 
        with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            # writing the fields 
            csvwriter.writerow(fields) 
                
            # writing the data rows 
            csvwriter.writerows(data)
        data = []
        filename = f"scenes/goal/scene{sceneNumber}Goal.csv"
        fields = ['1','2','3','4','5','6']
        arr = [-1,-1,-1,-1,-1,-1]
        for i in range(len(players)):
                arr[i] = players[i]['goal'][0]
        data.append(arr)
        arr = [-1,-1,-1,-1,-1,-1]
        for i in range(len(players)):
                arr[i] = players[i]['goal'][1]
        data.append(arr)


        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(data)

        filename = f"scenes/groups/scene{sceneNumber}Groups.csv"
        fields = ['1','2','3','4']
        data = []
        lst = []
        for i in range(groupNum):
            lst.append(groups[i+1])
        i = groupNum+1
        while i<=4:
            lst.append([-1])
            i+=1
        data.append(lst)
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(data)
        filename = f"scenes/obstacles/scene{sceneNumber}Obstacles.csv"
        fields = ['obstacles']
        data = []
        for i in range(len(obstacleList)):
            data.append([obstacleList[i]])
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(data)

        
        print('Data recording completed!')


    


def newPlayer(addr,sock):
    playerId, goal = game.addNewPlayer()
    game.playerNetId[addr] = {"playerId": playerId,"addr":addr}
    obstacles = []
    toSend = {
        "playerId": playerId,
        "arrMap": game.arrMap,
        "players": game.players,
        "goal": goal,
        "obstacles" : obstacles, 
    }
    sock.sendto(pickle.dumps(toSend),addr)
    # sock.sendto(pickle.dumps(game.arrMap),addr)
    # sock.sendto(pickle.dumps(game.players),addr)

start_new_thread(recordData, ())
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




