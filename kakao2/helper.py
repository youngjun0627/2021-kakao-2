def change_id_coord(id, N):
    return N-(id%N)-1, id//N

class Location(object):
    def __init__(self, problem, locations):
        self.N = 5 if problem==1 else 60
        self.board = [[0] * self.N for _ in range(self.N)]
        for location in locations:
            id, count = location['id'], location['located_bikes_count']
            y, x = change_id_coord(id, self.N)
            self.board[y][x] = count

    def get(self):
        return self.board


class Truck(object):
    def __init__(self, problem, truck, HOTPLACES):
        self.N = 5 if problem==1 else 60
        id, location_id, count = truck.get('id'), truck.get('location_id'), truck.get('loaded_bikes_count')
        y,x = change_id_coord(location_id, self.N)
        self.y = y
        self.x = x
        self.loaded_count = count
        self.count = 0
        self.id = id
        self.MAX_LOADED_COUNT = 5
        self.MIN_LOADED_COUNT = 2
        self.HOTPLACES = HOTPLACES
        self.MAX_COUNT = 10
        self.commands = []

    def check_count(self):
        if self.count<self.MAX_COUNT: return True
        return False

    def check_loaded_count(self):
        if self.loaded_count<self.MAX_LOADED_COUNT: return True
        return False

    def up(self):
        if not self.check_count() or self.y<=0: return
        self.y-=1
        self.commands.append(1)
        return

    def right(self):
        if not self.check_count() or self.x>=self.N-1: return
        self.x+=1
        self.commands.append(2)
        return

    def down(self):
        if not self.check_count() or self.y>=self.N-1: return
        self.y+=1
        self.commands.append(3)
        return

    def left(self):
        if not self.check_count() or self.x<=0: return
        self.x-=1
        self.commands.append(4)
        return

    def load(self, board, visit):
        if not self.check_count() or not self.check_loaded_count(): return
        self.loaded_count += 1
        self.count+=1
        y,x = self.y, self.x
        board[y][x]-=1
        visit[y][x]=True
        self.commands.append(5)
        return

    def unload(self, board, visit):
        if not self.check_count(): return
        self.loaded_count -= 1
        self.count+=1
        y,x = self.y, self.x
        board[y][x]+=1
        visit[y][x]=True
        self.commands.append(6)
        return

    def find_min(self, board, visit):
        n = self.N
        result = [0,0]
        _min = 9999999
        diff = 1000000
        for i in range(n):
            for j in range(n):
                if visit[i][j]: continue
                if _min<board[i][j]: continue
                if _min==board[i][j]:
                    if abs(i-self.y) + abs(j-self.x) < diff:
                        diff = abs(i-self.y) + abs(j-self.x)
                        result[0] = i
                        result[1] = j
                else:
                    _min = board[i][j]
                    result[0]=i
                    result[1]=j
                    diff = abs(i-self.y) + abs(j-self.x)
        return result[0], result[1], _min


    def find_max(self, board, visit):
        n = self.N
        result = [0,0]
        _max = 0
        diff = 10000000
        for i in range(n):
            for j in range(n):
                if visit[i][j]: continue
                if _max>board[i][j]: continue
                if _max==board[i][j]:
                    if abs(i-self.y) + abs(j-self.x) < diff:
                        diff = abs(i-self.y) + abs(j-self.x)
                        result[0] = i
                        result[1] = j
                else:
                    _max = board[i][j]
                    result[0]=i
                    result[1]=j
                    diff = abs(i-self.y) + abs(j-self.x)
        return result[0], result[1], _max

    def move(self, ey, ex):
        cy,cx = self.y, self.x
        if cy>ey:
            for _ in range(cy-ey):
                self.up()
        elif cy<ey:
            for _ in range(ey-cy):
                self.down()

        if cx>ex:
            for _ in range(cx-ex):
                self.left()
        elif cx<ex:
            for _ in range(ey-cy):
                self.right()

    def solution(self, board, visit):
        min_y, min_x, _min = self.find_min(board, visit)
        max_y, max_x, _max = self.find_max(board, visit)
        if self.loaded_count<=_max or self.loaded_count<=self.MIN_LOADED_COUNT:
            for _ in range(10):
                self.move(max_y, max_x)
            if self.HOTPLACES[self.y][self.x]:
                for _ in range(board[self.y][self.x]//4):
                    self.load(board, visit)
            else:
                for _ in range(board[self.y][self.x]//2):
                    self.load(board, visit)
        if self.loaded_count>_min:
            for _ in range(10):
                self.move(min_y, min_x)

            if self.HOTPLACES[self.y][self.x]:
                for _ in range(self.loaded_count):
                    self.unload(board, visit)
            else:
                for _ in range(self.loaded_count//2):
                    self.unload(board, visit)
        return self.commands


