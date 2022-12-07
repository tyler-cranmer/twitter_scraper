import os
import tweepy
import config
import json
from time import sleep
import random
import typing

def getClient() -> object:
    client = tweepy.Client(bearer_token=config.NFF33T_BEARER_TOKEN,
                        consumer_key=config.NFF33T_TWITTER_API_KEY, 
                        consumer_secret=config.NFF33T_TWITTER_API_SECRET_KEY, 
                        access_token=config.NFF33T_ACCESS_TOKEN, 
                        access_token_secret=config.NFF33T_ACCESS_TOKEN_SECRET,)
    return client

# Returns twitter user information
# username: a string of the username without @
def getUserInfo(username: str) -> object:
    client: object = getClient()
    user: object = client.get_user(username=username)
    return user


def writeJson(filepath: str, data: list) -> None:
    with open(filepath, 'w') as fp:
        json.dump(data,fp)


def readJson(filename: str) -> list[dict[str,str]]:
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
                # dic = {}
                # dic.update({"userName": user.username})
                # dic.update({"userID": str(user.id)})
                # followers.append(dic)
                info = (user.username, str(user.id))
                followers.append(info)
            break
        else:
            for user in users.data:
                # dic = {}
                # dic.update({"userName": user.username})
                # dic.update({"userID": str(user.id)})
                # followers.append(dic)
                info = (user.username, str(user.id))
                followers.append(info)
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
    unsuccess_count: int = 0
    success_count: int = 0
    client: object = getClient()
    people_to_follow: list[dict[str,str]] = readJson(f'{config.VPS_DIRECTORY}data/{toFollow}')
    already_following: list[dict[str,str]] = readJson(f'{config.VPS_DIRECTORY}data/{following}')
    if (len(people_to_follow) > 0):
            for user in people_to_follow:
                if (success_count > 399 or unsuccess_count > 50):
                    break
                elif (not user in already_following):
                    try:
                        client.follow_user(user['userID'])
                        already_following.append(user)
                        print(f'Successfully followed username: {user["userName"]}')
                        success_count +=1
                        sleep(20) # 50 calls per 15 min. ratelimit
                    except:
                        print(f'Trouble following username: {user["userName"]} userID: {user["userID"]}')
                        unsuccess_count +=1
                else:
                    print(f'Already Following {user["userName"]}')
    writeJson(f'{config.VPS_DIRECTORY}data/{following}', already_following)
    print(f'You successfully followed {success_count} accounts. \n There were {unsuccess_count} unsucessful follows.')

# This function unfollows up to 400 users in a given json file
# 
# unfollow: json file
# 
# Twitter API limit is 400 per 24h. So the function will unfollow the top 400
# users and then remove users from file for next fun
# 50 api calls per 15 min limit
def unFollow(unFollow: str) -> None:
    unsuccess_count: int = 0
    success_count: int = 0
    client: object = getClient()
    following: list[dict[str,str]] = readJson(f'{config.VPS_DIRECTORY}data/{unFollow}')
    if (len(following) > 0):
        for user in following:
            if(success_count >= 400 or unsuccess_count > 50):
                break
            else:
                try:
                    client.unfollow_user(user['userID'])
                    index: int = following.index(user)
                    following.pop(index)
                    success_count += 1
                    sleep(20) # 50 calls per 15 min. ratelimit
                except:
                    print(f'Trouble unfollowing username: {user["userName"]} userID: {user["userID"]}')
                    unsuccess_count += 1
    writeJson(f'{config.VPS_DIRECTORY}data/{unFollow}', following)
    print(f'You successfully followed {success_count} accounts. \n There were {unsuccess_count} unsucessful follows.')


if __name__ == '__main__':
    # people = [1304602369750003712, 1304602369750003712, 4286418493, 1472284812475920384]

    # dic = {}
    # for i, val1 in enumerate(people):
    #     l = getAllFollowers(val1, 1000)
    
    #     for j , val in enumerate(l):
    #         if val[0] not in dic:
    #             dic[val[0]] = 1
    #         else:
    #             dic[val[0]] += 1

    # sorted_dic = sorted(dic.items(), key=lambda x:x[1])
    # print(sorted_dic)
    people = [1304602369750003712, 4286418493]
    l = getUserFollowing(people[0], 100)
    print(l)