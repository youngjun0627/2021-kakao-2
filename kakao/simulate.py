import requests
import json
from startapi import startAPI
from locationapi import locationAPI
from truckapi import truckAPI
from helper import Truck, Board
from scoreapi import scoreAPI

def simulateAPI(auth_key, N):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/simulate'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'
    }
    def set_data(data):
        #dic_commands = {'no':0, 'up':1, 'right':2, 'down':3, 'left':4, 'stack':5, 'unstack':6}
        commands = {'commands':[]}
        for _data in data:
            commands['commands'].append({"truck_id":_data['truck_id'],"command":_data['command']})
        return json.dumps(commands)
    locations = locationAPI(auth_key)
    trucks = truckAPI(auth_key)
    board = Board(N, locations).get()
    for b in board:
        print(b)
    trucks = [Truck(id, trucks[id][0], trucks[id][1], N) for id in trucks]
    visit = [[False]*N for _ in range(N)]
    commands = []
    for truck in trucks:
        temp_y, temp_x = truck.y, truck.x
        result = truck.choice(board,visit)
        commands.append({'truck_id':truck.id, 'command':result})
    for c in commands:
        print(c)
    data = set_data(commands)
    response = requests.put(url = url, headers = headers, data = data)
    response = response.json()
    status = response['status']
    time = response['time']
    failed_requests_count = response['failed_requests_count']
    distance = response['distance']
    return [status, time, failed_requests_count, distance]

if __name__=='__main__':
    auth_key = startAPI(2)
    #commands = [{ "truck_id": 0, "command": [2, 5, 4, 1, 6] }]
    commands = [{ "truck_id": 0, "command": [] },
            { "truck_id": 1, "command": [] }]
    time=0
    while True:
        result = simulateAPI(auth_key,60)
        print(result)
        if result[0]=='finished':
            print(scoreAPI(auth_key))
            break
        time+=1
