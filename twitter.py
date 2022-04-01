import os
import tweepy
import config


def getClient():
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                        consumer_key=config.TWITTER_API_KEY, 
                        consumer_secret=config.TWITTER_API_SECRET_KEY, 
                        access_token=config.ACCESS_TOKEN, 
                        access_token_secret=config.ACCESS_TOKEN_SECRET,)
    return client

def getUserInfo(username: str):
    client = getClient()
    user = client.get_user(username=username)
    return user.data

if __name__ == '__main__':

   print(getUserInfo('tyler_cranmer'))
