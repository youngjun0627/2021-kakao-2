from API import startAPI, locationsAPI, trucksAPI, simulateAPI, scoreAPI
from helper import change_location_to_board, Truck
from analysis import choice
import time

def main(problem_id):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
    n = 5 if problem_id==1 else 60
    key = startAPI(url, problem_id)
    hotplaces = choice(problem_id)
    try:
        while True:
            visit = [[False]*n for _ in range(n)]
            locations = locationsAPI(url, key)
            board = change_location_to_board(locations, problem_id)
            trucks = trucksAPI(url, key)
            trucks = [Truck(truck, problem_id, hotplaces) for truck in trucks]
            commands = []
            for truck in trucks:
                commands.append(truck.solution(board, visit))
            commands = {'commands': commands}
            result = simulateAPI(url, key, commands)
            print(result)
            time.sleep(0.5)
            if result['status']=='finished':
                print(scoreAPI(url, key))
                break
    except Exception as e:
        print(e)
        return
if __name__=='__main__':
    main(1)

