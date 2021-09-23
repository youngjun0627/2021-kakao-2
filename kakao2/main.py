from API import startAPI, locationAPI, truckAPI, simulateAPI, scoreAPI
from helper import Location, Truck, change_id_coord
from analysis import choice

def main(problem):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
    key = startAPI(url, problem)
    n = 5 if problem==1 else 60
    HOTPLACES = [[0]*n for _ in range(n)]
    if problem==2:
        hot_places = choice(problem)
        for _id in hot_places:
            y,x = change_id_coord(_id, n)
            HOTPLACES[y][x] = 1
    while True:
        locations = locationAPI(url, key)
        locations = Location(problem, locations)
        board = locations.get()
        trucks = truckAPI(url, key)
        #for b in board:
        #    print(b)
        #print(trucks)
        trucks = [Truck(problem, truck, HOTPLACES) for truck in trucks]
        commands = []
        visit = [[False]*n for _ in range(n)]
        for truck in trucks:
            commands.append({'truck_id':truck.id, 'command':truck.solution(board, visit)})
        result = simulateAPI(url, key, commands)
        print(result)
        if result['status']=='finished':
            print(scoreAPI(url, key))
            break
if __name__ == '__main__':
    #main(1)
    main(2)
    

