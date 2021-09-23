import requests
import json
from startapi import startAPI

def truckAPI(auth_key):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/trucks'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'
    }
    response = requests.get(url = url, headers = headers)
    response = response.json()
    trucks = response['trucks']
    dic = {}
    for truck in trucks:
        id = truck.get('id')
        location_id = truck.get('location_id')
        loaded_bikes_count = truck.get('loaded_bikes_count')
        dic[id] = [location_id, loaded_bikes_count]
    return dic

if __name__=='__main__':
    auth_key = startAPI()
    print(truckAPI(auth_key))
