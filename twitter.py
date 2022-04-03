import os
import tweepy
import config
import json
from time import sleep


def getClient() -> object:
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                        consumer_key=config.TWITTER_API_KEY, 
                        consumer_secret=config.TWITTER_API_SECRET_KEY, 
                        access_token=config.ACCESS_TOKEN, 
                        access_token_secret=config.ACCESS_TOKEN_SECRET,)
    return client

# Returns twitter user information
# username: a string of the username without @
def getUserInfo(username: str) -> object:
    client: object = getClient()
    user: object = client.get_user(username=username)
    return user


def writeJson(filepath: str, data: list) -> json:
    with open(filepath, 'w') as fp:
        json.dump(data,fp)


def readJson(filename: str) -> json:
    with open(filename, 'r', encoding='utf-8') as fp:
        return json.load(fp)

# Returns a list of all the users followers
# _id: userID
# _max_results: 1 to 1000; max is 1000 users per page
#
# This function has a ratelimit built in. No more than 15 api calls per 15 minutes. 
def getAllFollowers(_id: int, _max_results: int) -> list:
    count: int = 1
    client: object = getClient()
    users: object = client.get_users_followers(id=_id, max_results=_max_results)
    followers: list = []
    while True:
        if (count % 15 == 0):
            sleep(60*15)  # Wait for 15 minutes
        elif('next_token' not in users.meta):
            for user in users.data:
                dic = {}
                dic.update({"userName": user.username})
                dic.update({"userID": str(user.id)})
                followers.append(dic)
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

# Returns a list of all the accounts the user is following.
# _id: userID
# _max_results: 1 to 1000; max is 1000 users per page
#
# This function has a ratelimit built in. No more than 15 api calls per 15 minutes. 
def getUserFollowing(_id: int, _max_results: int) -> list:
    count: int = 1
    client: object = getClient()
    users: object = client.get_users_following(id=_id, max_results=_max_results)
    followers: list = []
    while True:
        if (count % 15 == 0):
            sleep(60*15)  # Wait for 15 minutes
        elif('next_token' not in users.meta):
            for user in users.data:
                dic = {}
                dic.update({"userName": user.username})
                dic.update({"userID": str(user.id)})
                followers.append(dic)
            break
        else:
            for user in users.data:
                dic = {}
                dic.update({"userName": user.username})
                dic.update({"userID": str(user.id)})
                followers.append(dic)
            users = client.get_users_following(id=_id, max_results=_max_results, pagination_token= users.meta['next_token'])
        count += 1
    return followers

# This function will follow all the users of a given json object
# toFollow : json file of usernames and userIDs to follow
# following: json file of usernames and userIDs the account is already following
# will not follow usernames that are already in the following json file.
# updates following file with new list of usernames that are now following         
def follow(toFollow: str, following: str) -> None:
    count: int = 0
    client: object = getClient()
    people_to_follow: list[dict] = readJson(f'{config.VPS_DIRECTORY}data/{toFollow}')
    already_following: list[dict] = readJson(f'{config.VPS_DIRECTORY}data/{following}')
    if (len(people_to_follow) > 0 and count <= 400):
        for user in people_to_follow:
            if not user in already_following:
                try:
                    client.follow_user(user['userID'])
                    already_following.append(user)
                    print(f'Successfully followed username: {user["userName"]}')
                    count += 1
                    sleep(5)
                except:
                    print(f'Trouble following username: {user["userName"]} userID: {user["userID"]}')
            else:
                print(f'Already Following {user["userName"]}')
    writeJson(f'{config.VPS_DIRECTORY}data/{following}', already_following)



if __name__ == '__main__':
    peter = 1304602369750003712
    tyler_id = 4286418493
    follow('petersFollowing.json', 'tylersFollowing.json')
    # filepath = '{}/data/tylersFollowing.json'.format(config.VPS_DIRECTORY)
    # writeJson(filepath, followers)