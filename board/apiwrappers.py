from requests import get, post


API_IGDB_URL = 'https://api.igdb.com/v4/'
API_TWITTER_URL = 'https://api.twitter.com/2/'


class BaseWrapper:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self._requests_method = get

    def _api_request(self, endpoint, query):
        url = self._build_url(endpoint)
        params = self._compose_request(query)
        response = self._requests_method(url, **params)
        response.raise_for_status()

        return response.json()

    @staticmethod
    def _build_url(endpoint=''):
        return f'{API_TWITTER_URL}{endpoint}'

    def _compose_request(self, query):
        request_params = {
            'headers': {
                'Authorization': f'Bearer {self.auth_token}',
            }
        }
        request_params['params'] = query
        return request_params


class TwitterWrapper(BaseWrapper):
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
            return tweet_list

    def get_user_by_id(self, user_id):
        query = {
            'ids': user_id,
            'user.fields': 'id,username,url'
        }
        return self._get('users', query)[0]

    def _get(self, endpoint, query):
        response = self._api_request(endpoint, query)

        if 'data' in response:
            return response['data']
        else:
            return None


class IgdbWrapper(BaseWrapper):
    def __init__(self, client_id, auth_token):
        super().__init__(auth_token)
        self._requests_method = post
        self.client_id = client_id

    def get_games_by_id(self, game_id):
        query = {
            'fields': 'id, cover.image_id, name, '
                      'summary, screenshots.image_id, '
                      'genres.name, release_dates, '
                      'platforms.name, '
                      'aggregated_rating, aggregated_rating_count, '
                      'rating, rating_count, slug ',
            'filter[id][eq]': game_id
        }
        return self._post('games', query)

    def get_games_id(self, params):
        query = {
            'filter[screenshots][not_eq]': 'null',
            'filter[genres][not_eq]': 'null',
            **params
        }
        return self._post('games', query)

    def get_genres(self, query):
        return self._post('genres', query)

    def get_platforms(self, query):
        return self._post('platforms', query)

    @staticmethod
    def get_img_url(image_id, size='screenshot_big'):
        return 'https://images.igdb.com/igdb/image/upload/t_{}/{}.jpg'.format(size, image_id)

    @staticmethod
    def _build_url(endpoint=''):
        return f'{API_IGDB_URL}{endpoint}/'

    def _post(self, endpoint, query):
        return self._api_request(endpoint, query)

    def _compose_request(self, query):
        request_params = super()._compose_request(query)
        request_params['headers']['Client-ID'] = f'{self.client_id}'
        return request_params
