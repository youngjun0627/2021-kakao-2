import requests
import json
from startapi import startAPI
from locationapi import locationAPI
from truckapi import truckAPI
from collections import deque

def change_id_coord(id,N):
    return N-(id%N)-1, id//N

class Board(object):
    def __init__(self, N, locations):
        self.board = [[0] * N for _ in range(N)]
        for location in locations.items():
            id, count = location
            y, x = change_id_coord(id,N)
            self.board[y][x] = count

    def get(self):
        return self.board

class Truck(object):
    def __init__(self, id, location_id, loaded_count, N):
        self.id = id
        self.N = N
        self.loaded_count = loaded_count
        self.location = 0
        self.y, self.x = change_id_coord(location_id, self.N)
        self.command = []
        self.count = 0
        self.MAX_COUNT = 10
        self.MAX_LOADED_COUNT = 20
        self.average = 3

    def canMove(self):
        return True if self.count<self.MAX_COUNT else False
    
    def canLoad(self):
        return True if self.loaded_count<self.MAX_LOADED_COUNT else False

    def up(self):
        if not self.canMove() or self.y<=0: return
        self.command.append(1)
        self.count+=1
        self.y-=1
    
    def right(self):
        if not self.canMove() or self.x>=self.N-1: return
        self.command.append(2)
        self.count+=1
        self.x+=1

    def down(self):
        if not self.canMove() or self.y>=self.N-1: return
        self.command.append(3)
        self.count+=1
        self.y+=1

    def left(self):
        if not self.canMove() or self.x<=0: return
        self.command.append(4)
        self.count+=1
        self.x-=1

    def load(self, board):
        if not self.canMove() or not self.canLoad(): return
        y,x = change_id_coord(self.id, self.N)
        self.command.append(5)
        self.count+=1
        self.loaded_count+=1
        board[self.y][self.x]-=1
    
    def unload(self, board):
        if not self.canMove() or self.loaded_count<=0: return
        self.command.append(6)
        self.count+=1
        self.loaded_count-=1
        board[self.y][self.x]+=1

    def findmin(self, board, visit):
        coord = [0,0]
        diff = len(board) * len(board)
        for i in range(self.N):
            for j in range(self.N):
                if visit[i][j]: continue
                if board[i][j]==0 and abs(i-self.y)+abs(j-self.x)<diff:
                    #diff = abs(i-self.y)+abs(j-self.x)
                    coord[0] = i
                    coord[1] = j
        if self.y>coord[0]:
            for _ in range(self.y-coord[0]):
                self.up()
        else:
            for _ in range(coord[0]-self.y):
                self.down()
        if self.x>coord[1]:
            for _ in range(self.x-coord[1]):
                self.left()
        else:
            for _ in range(coord[1] - self.x):
                self.right()
        visit[coord[0]][coord[1]] = True

    def findmax(self, board, visit):
        coord = [0,0]
        diff = len(board) * len(board)
        for i in range(self.N):
            for j in range(self.N):
                if visit[i][j]: continue
                if board[i][j]>self.average and abs(i-self.y)+abs(j-self.x)<diff:
                    diff = abs(i-self.y)+abs(j-self.x)
                    coord[0] = i
                    coord[1] = j
        if self.y>coord[0]:
            for _ in range(self.y-coord[0]):
                self.up()
        else:
            for _ in range(coord[0]-self.y):
                self.down()
        if self.x>coord[1]:
            for _ in range(self.x-coord[1]):
                self.left()
        else:
            for _ in range(coord[1] - self.x):
                self.right()
        visit[coord[0]][coord[1]] = True

    def choice(self, board, visit):
        #if self.loaded_count>self.average:
        if board[self.y][self.x]==0 and self.loaded_count>0:
            while self.count<self.MAX_COUNT and board[self.y][self.x]<=self.average:
                self.unload(board)
                self.count+=1
        self.findmax(board, visit)
        while self.count<self.MAX_COUNT and board[self.y][self.x]>self.average:
            self.load(board)
            self.count+=1
        
        self.findmin(board, visit)

        while self.count<self.MAX_COUNT and board[self.y][self.x]<self.average:
            self.unload(board)
            self.count+=1
        return self.command
        #else: 

if __name__=='__main__':
    print(0)
