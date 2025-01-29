import tweepy
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bearer_token = os.getenv('BEARER_TOKEN')
client = tweepy.Client(bearer_token)


def get_latest_tweets(username):
    try:
        user = client.get_user(username=username)
        user_id = user.data.id
        response = client.get_users_tweets(user_id)

        tweets = []
        for tweet in response.data:
            tweets.append(tweet.get("text"))
        return tweets
    except tweepy.TooManyRequests as e:
        logging.exception(e)
        error = "Request limit exceeded."
        return error
    except Exception as e:
        logging.exception(e)
