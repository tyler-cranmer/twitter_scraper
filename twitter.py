import os
import tweepy
import config
import json
from time import sleep


def getClient() -> object:
    client = tweepy.Client(bearer_token=config.NFF33T_BEARER_TOKEN,
                        consumer_key=config.NFF33T_TWITTER_API_KEY, 
                        consumer_secret=config.NFF33T_TWITTER_API_SECRET_KEY, 
                        access_token=config.NFF33T_ACCESS_TOKEN, 
                        access_token_secret=config.NFF33T_TOKEN_SECRET,)
    return client

def getUserInfo(username: str) -> object:
    client: object = getClient()
    user: object = client.get_user(username=username)
    return user

tyler_id = 4286418493

def writeJson(filepath: str, data: list) -> json:
    with open(filepath, 'w') as fp:
        json.dump(data,fp)

def readJson(filename: str) -> json:
    with open(filename, 'r', encoding='utf-8') as fp:
        return json.load(fp)

def getAllFollowers(_id: int, _max_results: int) -> list:
    count: int = 1
    client: object = getClient()
    users: object = client.get_users_followers(id=_id, max_results=_max_results)
    followers: list = []
    while True:
        if (count % 15 == 0):
            sleep(60*15)  # Wait for 15 minutes
        elif('next_token' not in users.meta):
            break
        else:
            for user in users.data:
                dic = {}
                dic.update({"userName": user.username})
                dic.update({"userID": str(user.id)})
                followers.append(dic)
            users = client.get_users_followers(id=_id, max_results=_max_results, pagination_token= users.meta['next_token'])
        count += 1
    return followers
        
def follow(toFollow: str, following: str) -> None:
    count: int = 0
    client: object = getClient()
    people_to_follow: list[dict] = readJson(f'{config.VPS_DIRECTORY}data/{toFollow}')
    already_following: list[dict] = readJson(f'{config.VPS_DIRECTORY}data/{following}')
    if len(people_to_follow) > 0:
        for user in people_to_follow:
            if not user in already_following:
                try:
                    client.follow_user(user['userID'])
                    already_following.append(user)
                    print(f'Successfully followed username: {user["userName"]}')
                    sleep(5)
                except:
                    print(f'Trouble following username: {user["userName"]} userID: {user["userID"]}')
            else:
                print(f'Already Following {user["userName"]}')
    writeJson(f'{config.VPS_DIRECTORY}data/{following}', already_following)



if __name__ == '__main__':
    tyler = getUserInfo('tyler_cranmer')
    print(tyler)