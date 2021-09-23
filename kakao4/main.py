from API import startAPI, locationsAPI, trucksAPI, simulateAPI, scoreAPI
from helper import Locations, Truck
from analysis import choice

def main(problem_id):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
    token = startAPI(url, problem_id)
    MAX = 10000
    n = 5 if problem_id==1 else 60
    time = 0
    hotplaces = None
    while time<720:
        if time in [0, 240, 480]:
            hotplaces = choice(problem_id, time, time+240)
        locations = locationsAPI(url, token)
        trucks = trucksAPI(url, token)
        board = Locations(locations, n)
        board = board.get()
        trucks = [Truck(truck, n, hotplaces) for truck in trucks]
        visit = [[False] * n for _ in range(n)]
        commands = []
        for truck in trucks:
            command = truck.solution(board, visit)
            commands.append(command)
        commands = {'commands':commands}
        result = simulateAPI(url, token, commands)
        print(result)
        time+=1
        if result['status']=='finished':
            print(scoreAPI(url, token))
            break

if __name__=='__main__':
    problem_id = 2
    main(problem_id)


