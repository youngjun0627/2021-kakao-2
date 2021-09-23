import requests
import json

def scoreAPI(auth_key):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/score'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'
    }
    response = requests.get(url = url, headers = headers)
    print(response)
    response = response.json()
    print(response)
    return response['score']

if __name__=='__main__':
    for _ in range(720):
       auth_key = startAPI()
       a = locationAPI(auth_key)
       print(a)
