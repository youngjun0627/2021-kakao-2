import requests
import json

def startAPI(url, problem_id):
    x_token = '24dabc8e757c9f023994c5b9ec4a34e9'
    headers = {
            'X-Auth-Token': x_token,
            'Content-Type': 'application/json',
    }
    params = {'problem':problem_id}
    url = url+'/start'
    resp = requests.post(url=url, headers = headers, params = params).json()
    return resp['auth_key']

def locationsAPI(url, key):
    url = url + '/locations'
    headers = {
            'Authorization': key,
            'Content-Type': 'application/json',
    }
    resp = requests.get(url=url, headers=headers).json()
    return resp['locations']

def trucksAPI(url, key):
    url = url + '/trucks'
    headers = {
            'Authorization': key,
            'Content-Type': 'application/json',
    }
    resp = requests.get(url=url, headers=headers).json()
    return resp['trucks']

def simulateAPI(url, key, commands):
    url = url + '/simulate'
    headers = {
            'Authorization': key,
            'Content-Type': 'application/json',
    }
    resp = requests.put(url=url, headers=headers, data = json.dumps(commands))
    return resp.json()

def scoreAPI(url, key):
    url = url + '/score'
    headers = {
            'Authorization': key,
            'Content-Type': 'application/json',
    }

    resp = requests.get(url=url, headers=headers)
    return resp.json()

if __name__=='__main__':
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
    key = startAPI(url, 1)
    print(locationsAPI(url, key))
    print(trucksAPI(url, key))
