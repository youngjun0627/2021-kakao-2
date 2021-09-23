def change_id_coord(id, n):
    return n-(id%n)-1,id//n

class Locations(object):
    def __init__(self, locations, n):
        self.n = n
        self.board = [[0] * self.n for _ in range(self.n)]
        for location in locations:
            y,x = change_id_coord(location['id'], self.n)
            self.board[y][x] = location['located_bikes_count']

    def get(self):
        return self.board

class Truck(object):
    def __init__(self, truck, n, hotplaces):
        self.id = truck['id']
        self.n = n
        self.y,self.x = change_id_coord(truck['location_id'], self.n)
        self.count = 0
        self.loaded_count = truck['loaded_bikes_count']
        self.MAX_COUNT = 10
        self.MAX_LOADED_COUNT = 20
        self.commands = []

        # problem 2
        if hotplaces:
            self.lend_places = []
            for place in hotplaces[0]:
                self.lend_places.append(change_id_coord(place, self.n))
            self.return_places = []
            for place in hotplaces[1]:
                self.return_places.append(change_id_coord(place, self.n))


    def check_count(self):
        return True if self.count<self.MAX_COUNT else False

    def check_loaded_count(self):
        return True if self.loaded_count<self.MAX_LOADED_COUNT else False

    def no(self):
        if not self.check_count(): return False
        self.count+=1
        self.commands.append(0)
        return True

    def up(self):
        if not self.check_count(): return False
        self.count+=1
        self.commands.append(1)
        self.y-=1
        return True

    def right(self):
        if not self.check_count(): return False
        self.count+=1
        self.commands.append(2)
        self.x+=1
        return True

    def down(self):
        if not self.check_count(): return False
        self.count+=1
        self.commands.append(3)
        self.y+=1
        return True

    def left(self):
        if not self.check_count(): return False
        self.count+=1
        self.commands.append(4)
        self.x-=1
        return True

    def load(self):
        if not self.check_count(): return False
        if not self.check_loaded_count(): return False
        self.count+=1
        self.loaded_count+=1
        self.commands.append(5)
        return True

    def unload(self):
        if not self.check_count(): return False
        if self.loaded_count<=0: return False
        self.count+=1
        self.loaded_count-=1
        self.commands.append(6)
        return True

    def find_min(self, board, visit):
        _min = 999999
        diff = 999999
        coord = [0,0]
        for i in range(self.n):
            for j in range(self.n):
                if visit[i][j]: continue
                if board[i][j]<_min:
                    _min = board[i][j]
                    coord[0]=i
                    coord[1]=j
                elif board[i][j]==_min:
                    temp = abs(self.y-i) + abs(self.x-j)
                    if diff>temp:
                        diff = temp
                        coord[0]=i
                        coord[1]=j
        return coord[0], coord[1], _min

    def find_max(self, board, visit):
        _max = 0
        diff = 999999
        coord = [0,0]
        for i in range(self.n):
            for j in range(self.n):
                if visit[i][j]: continue
                if board[i][j]>_max:
                    _max = board[i][j]
                    coord[0]=i
                    coord[1]=j
                elif board[i][j]==_max:
                    temp = abs(self.y-i) + abs(self.x-j)
                    if diff>temp:
                        diff = temp
                        coord[0]=i
                        coord[1]=j
        return coord[0], coord[1], _max

    def find_mean(self, board, visit):
        result = 0
        cnt = 0
        for i in range(self.n):
            for j in range(self.n):
                if visit[i][j]: continue
                result+=board[i][j]
                cnt+=1
        return result//(self.n * self.n)

    def move(self, ey, ex):
        y, x = self.y, self.x
        if ey>y:
            for _ in range(ey-y):
                if not self.down(): return False
        elif ey<y:
            for _ in range(y-ey):
                if not self.up(): return False
        if ex>x:
            for _ in range(ex-x):
                if not self.right(): return False
        elif ex<x:
            for _ in range(x-ex):
                if not self.left(): return False
        return True

    def get(self):
        return {'truck_id': self.id, 'command': self.commands}

    def solution(self, board, visit):
        min_y,min_x,_min = self.find_min(board, visit)
        if self.loaded_count>_min:
            if self.move(min_y,min_x):
                if (min_y, min_x) in self.lend_places:
                    cnt = ((self.loaded_count+1)*3)//4
                else:
                    cnt = (self.loaded_count+1)//2
                for _ in range(cnt):
                    if self.unload():
                        board[min_y][min_x]+=1
                        visit[min_y][min_x]=True

        max_y,max_x,_max = self.find_max(board, visit)
        mean = self.find_mean(board, visit)
        if self.loaded_count<mean:
            if self.move(max_y, max_x):
                if (max_y, max_x) in self.return_places:
                    cnt = (board[max_y][max_x]*3)//4
                else:
                    cnt = board[max_y][max_x]//2
                for _ in range(cnt):
                    if self.load():
                        board[max_y][max_x]-=1
                        visit[max_y][max_x]=True

        return self.get() 
