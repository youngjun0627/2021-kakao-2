import requests
import json

def func(i,j):
    url = 'https://grepp-cloudfront.s3.ap-northeast-2.amazonaws.com/programmers_imgs/competition-imgs/2021kakao/problem{0}_day-{1}.json'.format(i,j)
    response = requests.get(url = url)
    response = response.json()
    dic = {}
    for k,v in response.items():
        for a in v:
            if a[0] not in dic:
                dic[a[0]]=0
            dic[a[0]]+=1
    result = {}
    for k, v in dic.items():
        if v>10:
            result[k]=v
    return list(result.keys())

def choice(problem):
    arr = set()
    i = problem
    for j in range(1,4):
        arr = arr.union(set(func(i,j)))
    return list(arr)
