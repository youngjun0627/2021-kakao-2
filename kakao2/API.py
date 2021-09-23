import requests
import json

def startAPI(url, problem):
    params = {"problem":problem}
    Token = '4a862ccef9381965a9ed0c43c8029456'
    url = url + '/start'
    headers = {'X-auth-Token': str(Token),
            'Content-Type': 'application/json'}
    response = requests.post(url = url, headers = headers, data = json.dumps(params))
    response = response.json()
    return response['auth_key']

def locationAPI(url, auth_key):
    url = url + '/locations'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'}
    response = requests.get(url = url, headers = headers)
    response = response.json()
    return response['locations']

def truckAPI(url, auth_key):
    url = url + '/trucks'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'}
    response = requests.get(url = url, headers = headers)
    response = response.json()
    return response['trucks']

def simulateAPI(url, auth_key, params):
    url = url + '/simulate'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'}
    params = {"commands": params}
    params = json.dumps(params)
    response = requests.put(url = url, headers = headers, data = params)
    response = response.json()
    return response

def scoreAPI(url, auth_key):
    url = url + '/score'
    headers = {'Authorization': auth_key,
            'Content-Type': 'application/json'}
    response = requests.get(url = url, headers = headers)
    response = response.json()
    return response['score']

if __name__=='__main__':
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
    key = startAPI(url, 1)
    print(key)
    print(locationAPI(url, key))
    print(truckAPI(url, key))
    #print(simulateAPI(url, key))
    #print(locationAPI(url, key))
