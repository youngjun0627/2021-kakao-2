import requests
import json

def startAPI(url, problem_id):
    url = url + '/start'
    x_auth_token = '24dabc8e757c9f023994c5b9ec4a34e9'
    data = {'problem': problem_id}
    resp = requests.post(url = url,
            headers = {
                'X-auth-Token': x_auth_token,
                'Content-Type': 'application/json',
            },
            #params = data
            data = json.dumps(data),
    )
    resp = resp.json()
    return resp['auth_key']

def locationsAPI(url, auth_key):
    url = url + '/locations'
    resp = requests.get(url = url,
            headers = {
                'Authorization': auth_key,
                'Content-Type': 'application/json',
            },
    )
    resp = resp.json()
    return resp['locations']

def trucksAPI(url, auth_key):
    url = url + '/trucks'
    resp = requests.get(url = url,
            headers = {
                'Authorization': auth_key,
                'Content-Type': 'application/json',
            },
    )
    resp = resp.json()
    return resp['trucks']


def simulateAPI(url, auth_key, commands):
    url = url + '/simulate'
    resp = requests.put(url = url,
            headers = {
                'Authorization': auth_key,
                'Content-Type': 'application/json',
            },
            data = json.dumps(commands),
    )
    resp = resp.json()
    return resp


def scoreAPI(url, auth_key):
    url = url + '/score'
    resp = requests.get(url = url,
            headers = {
                'Authorization': auth_key,
                'Content-Type': 'application/json',
            },
    )
    resp = resp.json()
    return resp


if __name__=='__main__':
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
    problem_id = 1
    token = startAPI(url, problem_id)
    print(token)
    
