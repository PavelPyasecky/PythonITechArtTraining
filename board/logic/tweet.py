import gamestore.settings as settings
from board.api import twitterapi


twitter_wrapper = twitterapi.TwitterWrapper(settings.API_TWITTER_TOKEN)


class Tweet:
    def __init__(self, tweet_id):
        tweet = twitter_wrapper.get_tweet_by_id(tweet_id)
        self.id = tweet["id"]
        self.text = tweet["text"]
        self.created_at = tweet["created_at"]
        self.author_id = tweet["author_id"]
        user = twitter_wrapper.get_user_by_id(self.author_id)
        self.author_name = user["username"]
        self.author_url = user["url"]
