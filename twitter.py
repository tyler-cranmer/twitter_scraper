import os
import tweepy
import config
import json


def getClient() -> object:
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                        consumer_key=config.TWITTER_API_KEY, 
                        consumer_secret=config.TWITTER_API_SECRET_KEY, 
                        access_token=config.ACCESS_TOKEN, 
                        access_token_secret=config.ACCESS_TOKEN_SECRET,)
    return client

def getUserInfo(username: str) -> object:
    client: object = getClient()
    user: object = client.get_user(username=username)
    return user

def getFollowers(_id: int, _max_results: int) -> list:
    client: object = getClient()
    users: object = client.get_users_followers(id=_id, max_results=_max_results)
    list_followers: list = []
    for user in users.data:
       dic = {}
       dic.update({"userName": user.username})
       dic.update({"userID": str(user.id)})
       list_followers.append(dic)
    return list_followers

tyler_id = 4286418493

def pagFollowers(_id: int, _max_results: int, _pagination:str):
    client: object = getClient()
    users: object = client.get_users_followers(id=_id, max_results=_max_results, pagination_token= _pagination)
    followers: list = []
    dic: dict = {}
    if 'next_token' not in users.meta:
        next_token: str = ''
    else: 
        next_token = users.meta['next_token']
    for user in users.data:
        dic = {}
        dic.update({"userName": user.username})
        dic.update({"userID": str(user.id)})
        followers.append(dic)

    if len(next_token) != 0:
        return pagFollowers(_id, _max_results, next_token)
    else:
        return followers

def writeJson(filepath: str, data: list) -> json:
    with open(filepath, 'w') as fp:
        json.dump(data,fp)

def readJson(filename: str) -> json:
    with open(filename, 'r', encoding='utf-8') as fp:
        return json.load(fp)

def getAllFollowers(_id: int, _max_results: int):
    client: object = getClient()
    users: object = client.get_users_followers(id=_id, max_results=_max_results)
    followers: list = []
    while True:
        for user in users.data:
            dic = {}
            dic.update({"userName": user.username})
            dic.update({"userID": str(user.id)})
            followers.append(dic)
        users = client.get_users_followers(id=_id, max_results=_max_results, pagination_token= users.meta['next_token'])
        if('next_token' not in users.meta):
            for user in users.data:
                dic = {}
                dic.update({"userName": user.username})
                dic.update({"userID": str(user.id)})
                followers.append(dic)
            break
    return followers
        

if __name__ == '__main__':

    pag = getAllFollowers(tyler_id, 25)
    print(pag)
    print(len(pag))
