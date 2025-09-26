import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()


twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)


def scrape_user_tweets(username, num_tweets=5):
    """Scrape a Twitter user's original tweets using the Twitter API.

    Fetches the user's original tweets (excluding retweets and replies)
    and returns them as a structured list.

    Args:
        username (str): Twitter username (without @ prefix).
        num_tweets (int): Maximum number of tweets to retrieve. Default is 5.

    Returns:
        list[dict]: List of tweet dictionaries, each containing:
                   - 'text': The tweet content
                   - 'url': Direct URL to the tweet
    """
    user_id = twitter_client.get_user(username=username).data.id
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )

    tweet_list = []
    for tweet in tweets.data:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
        tweet_list.append(tweet_dict)

    return tweet_list


def scrape_user_tweets_mock(username="EdenEmarco177", num_tweets=5):
    """Scrape mock Twitter data from a GitHub Gist for testing purposes.

    Uses a pre-made collection of Eden Marco's tweets from a GitHub Gist
    instead of calling the real Twitter API. Useful for testing and
    development without API rate limits.

    Args:
        username (str): Twitter username to use in generated URLs.
                       Default is "EdenEmarco177".
        num_tweets (int): Number of tweets to return (not currently used,
                         returns all tweets from the gist). Default is 5.

    Returns:
        list[dict]: List of tweet dictionaries, each containing:
                   - 'text': The tweet content
                   - 'url': Direct URL to the tweet

    Note:
        Source: https://twitter.com/EdenEmarco177
    """
    EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json"
    tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()

    tweet_list = []
    for tweet in tweets:

        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":

    tweets = scrape_user_tweets_mock(username="EdenEmarco177")
    print(tweets)
