def change_id_coord(id, problem):
    n = 5 if problem==1 else 60
    return n-1-(id%n), id//n


def change_location_to_board(locations, problem):
    n = 5 if problem==1 else 60
    board = [[0] * n for _ in range(n)]
    for location in locations:
        id, count = location['id'], location['located_bikes_count']
        y, x = change_id_coord(id, problem)
        board[y][x] = count
    return board

class Truck(object):
    def __init__(self, truck, problem, hotplaces):
        self.truck_id = truck['id']
        self.location_id = truck['location_id']
        self.loaded_count = truck['loaded_bikes_count']
        self.y, self.x = change_id_coord(self.location_id, problem)
        self.n = 5 if problem==1 else 60
        self.count = 0
        self.commands = []
        lend_place, return_place = hotplaces
        self.hot_lend_places = [[0] * self.n for _ in range(self.n)]
        self.hot_return_places = [[0] * self.n for _ in range(self.n)]
        if problem==2:
            for place in lend_place:
                y,x = change_id_coord(place, self.n)
                self.hot_lend_places[y][x]=1
            for place in return_place:
                y,x = change_id_coord(place, self.n)
                self.hot_return_places[y][x]=1
        self.MAX_COUNT = 10
        self.MAX_LOADED_COUNT = 20
        self.average = 2 if problem==1 else 3

    def check_count(self):
        if self.count<self.MAX_COUNT: return True
        return False

    def check_load_count(self):
        if self.loaded_count<self.MAX_LOADED_COUNT: return True
        return False

    def up(self):
        if not self.check_count(): return False
        if self.y==0: return False
        self.y -=1
        self.count+=1
        self.commands.append(1)
        return True

    def right(self):
        if not self.check_count(): return False
        if self.x==self.n-1: return False
        self.x+=1
        self.count+=1
        self.commands.append(2)
        return True
    
    def down(self):
        if not self.check_count(): return False
        if self.y==self.n-1: return False
        self.y +=1
        self.count+=1
        self.commands.append(3)
        return True

    def left(self):
        if not self.check_count(): return False
        if self.x==0: return False
        self.x-=1
        self.count+=1
        self.commands.append(4)
        return True

    def load(self, board):
        if not self.check_count(): return False
        if not self.check_load_count(): return False
        board[self.y][self.x]-=1
        self.loaded_count+=1
        self.count+=1
        self.commands.append(5)
        return True
    
    def unload(self, board):
        if not self.check_count(): return False
        if self.loaded_count==0: return False
        board[self.y][self.x]+=1
        self.loaded_count-=1
        self.count+=1
        self.commands.append(6)
        return True

    def find_min(self, board, visit):
        _min = 9999999
        diff = 9999999
        result = [0,0]
        for i in range(self.n):
            for j in range(self.n):
                if visit[i][j]: continue
                if board[i][j]<_min:
                    _min = board[i][j]
                    result[0] = i
                    result[1] = j
                elif board[i][j]==_min:
                    temp = abs(self.y-i) + abs(self.x-j)
                    if diff>temp:
                        diff = temp
                        result[0]=i
                        result[1]=j
        return result

    def find_max(self, board, visit):
        _max = -1
        diff = 9999999
        result = [0,0]
        for i in range(self.n):
            for j in range(self.n):
                if visit[i][j]: continue
                if board[i][j]>_max:
                    _max = board[i][j]
                    result[0] = i
                    result[1] = j
                elif board[i][j]==_max:
                    temp = abs(self.y-i) + abs(self.x-j)
                    if diff>temp:
                        diff = temp
                        result[0]=i
                        result[1]=j
        return result

    def move(self, ey, ex):
        y,x = self.y, self.x
        if ey>y:
            for _ in range(ey-y):
                self.down()
        elif ey<y:
            for _ in range(y-ey):
                self.up()
        if ex>x:
            for _ in range(ex-x):
                self.right()
        elif ex<x:
            for _ in range(x-ex):
                self.left()
        return self.check_count()

    def solution(self, board, visit):
        if self.loaded_count>0:
            ey, ex = self.find_min(board, visit)
            check = self.move(ey,ex)
            if check:
                if self.hot_lend_places[ey][ex]:
                    for _ in range(self.loaded_count):
                        self.unload(board)
                else:
                    for _ in range((self.loaded_count+1)//2):
                        self.unload(board)
                visit[ey][ex]=True
        if self.loaded_count<self.average:
            ey, ex = self.find_max(board, visit)
            check = self.move(ey,ex)
            if check:
                if self.hot_return_places[ey][ex]:
                    for _ in range(board[ey][ex]*3//4):
                        self.load(board)
                else:
                    for _ in range(board[ey][ex]//2):
                        self.load(board)
                visit[ey][ex] = True
        return {'truck_id': self.truck_id, 'command': self.commands}

if __name__=='__main__':
    print(change_id_coord(13,1))
