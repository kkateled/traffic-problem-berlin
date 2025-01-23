import tweepy
import os
import json


bearer_token = os.getenv('BEARER_TOKEN')
client = tweepy.Client(bearer_token)


def get_latest_tweets(username):
    user = client.get_user(username=username)
    user_id = user.data.id
    response = client.get_users_tweets(user_id)
    tweets = []
    for tweet in response.data:
        json_to_string = json.dumps(tweet.text)
        tweets.append(json_to_string)
    return tweets
