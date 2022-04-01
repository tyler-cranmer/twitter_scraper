import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

def scrape_user_followers(username):
    followers_scraped = []
    user = api.get_user(username)
    for i, _id in enumerate(tweepy.Cursor(api.followers_id, screen_name = username).items()):
        print(i, _id)
        followers_scraped.append(_id)
    return followers_scraped

if __name__ == '__main__':

    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    screenName = 52064008
    # response = client.get_users(usernames=['Iamamystreet'])
    # followers = client.get_users_followers(id=screenName, max_results=1000, pagination_token=next_token)   
    # l = []    
    scrape_user_followers(screenName) 
