import requests
import json
from startapi import startAPI
def locationAPI(auth_key):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/locations'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'
    }
    response = requests.get(url = url, headers = headers)
    response = response.json()
    locations = response['locations']
    dic = {}
    for location in locations:
        id, located_bikes_count = location['id'], location['located_bikes_count']
        dic[id] = located_bikes_count
    return dic

if __name__=='__main__':
    for _ in range(720):
       auth_key = startAPI()
       a = locationAPI(auth_key)
       print(a)
