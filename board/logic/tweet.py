import datetime
import gamestore.settings as settings
from board.api import twitterapi
from board.models import Tweet as TweetModel, Game
from django.utils.timezone import make_aware


twitter_wrapper = twitterapi.TwitterWrapper(settings.API_TWITTER_TOKEN)


class TweetAPI:
    def __init__(self, tweet_id):
        tweet = twitter_wrapper.get_tweet_by_id(tweet_id)
        self.id = tweet['id']
        self.text = tweet['text']
        self.created_at = tweet['created_at']
        self.author_id = tweet['author_id']
        user = twitter_wrapper.get_user_by_id(self.author_id)
        self.author_name = user['username']
        self.author_url = user['url']


class Tweet:
    def __init__(self, tweet_id):
        tweet = TweetModel.objects.get(id=tweet_id)
        self.id = tweet.id
        self.text = tweet.text
        self.created_at = make_aware(datetime.datetime.fromtimestamp(tweet.created_at))
        self.author_id = tweet.author_id
        self.author_name = tweet.author_name
        self.author_url = tweet.author_url

    @staticmethod
    def get_tweets(game_id):
        game = Game.objects.filter(id=game_id).first()
        tweets = game.tweets.all()
        if tweets:
            return tweets
        return None
