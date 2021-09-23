import requests
import json

def startAPI(problem):
    url = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users/start'
    headers = {'X-Auth-Token': '31cc80b353b4a9d9c39400e2ea7d3673',
            'Content-Type': 'application/json'
    }
    data =' {"problem":2}'
    print(data)
    response = requests.post(url = url, headers = headers, data = data)
    print(response)
    response = response.json()
    return response.get('auth_key')

if __name__=='__main__':
    startAPI()
