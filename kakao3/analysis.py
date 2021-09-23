import requests
import json

def choice(problem_id):
    lend_dic = {}
    return_dic = {}
    for day in range(1,4):
        url = 'https://grepp-cloudfront.s3.ap-northeast-2.amazonaws.com/programmers_imgs/competition-imgs/2021kakao/problem{0}_day-{1}.json'.format(problem_id, day)
        resp = requests.get(url=url)
        resp = resp.json()

        for _, v in resp.items():
            for a, b, _ in v:
                if a not in lend_dic:
                    lend_dic[a] = 0
                if b not in return_dic:
                    return_dic[b] = 0
                lend_dic[a]+=1
                return_dic[b]+=1
    result1 = []
    result2 = []
    for k,v in lend_dic.items():
        if v>100:
            result1.append(k)
    for k,v in return_dic.items():
        if v>100:
            result2.append(k)
    return result1, result2

if __name__=='__main__':
    choice(1)

