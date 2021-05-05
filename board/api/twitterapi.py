from board.api.base import BaseWrapper
from requests import get

API_TWITTER_URL = 'https://api.twitter.com/2/'


class TwitterWrapper(BaseWrapper):
    def __init__(self, auth_token):
        super().__init__(API_TWITTER_URL)
        self._auth_token = auth_token

    def get_tweet_by_id(self, tweet_id):
        query = {
            'tweet.fields': 'id,created_at,author_id'
        }
        return self._get(f'tweets/{tweet_id}', query)

    def get_tweets_by_string(self, key_word):
        query = {
            'tweet.fields': 'id',
            'query': f'{key_word} lang:en',
        }
        tweet_list = self._get('tweets/search/recent', query)
        if tweet_list:
            return [item['id'] for item in tweet_list]
        else:
            return None

    def get_user_by_id(self, user_id):
        query = {
            'ids': user_id,
            'user.fields': 'id,username,url'
        }
        return self._get('users', query)[0]

    def _get(self, endpoint, query):
        response = self._api_request(endpoint, query, get)

        if 'data' in response:
            return response['data']
        else:
            return None

    def _compose_request(self, query):
        request_params = {
            'headers': {
                'Authorization': f'Bearer {self._auth_token}',
            }
        }
        request_params['params'] = query
        return request_params
