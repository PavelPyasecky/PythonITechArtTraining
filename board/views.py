import os
import datetime
from requests import post
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


API_IGDB_URL = 'https://api.igdb.com/v4/'


class IGDB:
    def __init__(self, client_id, auth_token):
        self.client_id = client_id
        self.auth_token = auth_token

    def api_request(self, endpoint, query):
        url = IGDB._build_url(endpoint)
        params = self._compose_request(query)
        response = post(url, **params)
        response.raise_for_status()

        return response.json()

    def get_games(self, query):
        return self.api_request('games', query)

    def get_genres(self, query):
        return self.api_request('genres', query)

    def get_platforms(self, query):
        return self.api_request('platforms', query)

    @staticmethod
    def _build_url(endpoint=''):
        return f'{API_IGDB_URL}{endpoint}/'

    def _compose_request(self, query):
        if not query:
            raise Exception('No query provided!')
        request_params = {
            'headers': {
                'Client-ID': f'{self.client_id}',
                'Authorization': f'Bearer {self.auth_token}',
            }
        }

        if isinstance(query, dict):
            request_params['params'] = query
            return request_params

        raise TypeError('Incorrect type of argument "query"')


wrapper = IGDB(os.getenv('API_CLIENT_ID'), os.getenv('API_SECRET_KEY'))


def get_img_url(image_id, size='screenshot_big'):
    return 'https://images.igdb.com/igdb/image/upload/t_{}/{}.jpg'.format(size, image_id)


class Game:
    def __init__(self, game_id):
        params = {
            'fields': 'id, cover.image_id, name, '
                      'summary, screenshots.image_id, '
                      'genres.name, release_dates, '
                      'platforms.name, '
                      'aggregated_rating, aggregated_rating_count, '
                      'rating, rating_count ',
            'filter[id][eq]': game_id
        }

        res = wrapper.get_games(params)[0]

        self.id = game_id
        self.name = res['name']
        self.full_description = res['summary']
        if 'cover' in res:
            self.img_url = get_img_url(res['cover']['image_id'])
        else:
            self.img_url = get_img_url(res['screenshots'][0]['image_id'])
        if 'release_dates' in res:
            self.release = datetime.datetime.fromtimestamp(res['release_dates'][0])
        else:
            self.release = '--.--.--'
        self.screen_url = [get_img_url(item['image_id']) for item in res['screenshots']]
        self.genres = [genre['name'] for genre in res['genres']]
        self.platforms = [platform['name'] for platform in res['platforms']] if res.get('platforms') else []
        if 'rating' in res:
            self.rating = [res['rating'], res['rating_count']]
        else:
            self.rating = ['', 0]
        if 'aggregated_rating' in res:
            self.aggregated_rating = [res['aggregated_rating'], res['aggregated_rating_count']]
        else:
            self.aggregated_rating = ['', 0]

    tweets = [['tweet_name',
               'Pac-Man is a maze arcade game developed and released by Namco in 1980.'
               'The original Japanese title of Puck Man was changed to Pac-Man for international releases as '
               'a preventative',
               datetime.datetime.now()]] * 5


class Filter:
    def __init__(self):
        params = {
            'fields': 'name'
        }
        res_genres = wrapper.get_genres(params)
        res_platforms = wrapper.get_platforms(params)

        self.genres = res_genres
        self.genres.insert(0, {'id': 0, 'name': 'Any'})
        self.platforms = res_platforms


def main(request):
    params_post = {}
    initials = {}

    data = request.GET

    if 'platforms' in data:
        params_post['filter[platforms][eq]'] = '(' + ','.join(data.getlist('platforms')) + ')'
        initials['platforms'] = [int(item) for item in data.getlist('platforms')]
    if 'genres' in data:
        if data['genres'] != '0':
            initials['genres'] = params_post['filter[genres][eq]'] = int(data['genres'])
    if 'rating' in data:
        initials['rating'] = params_post['filter[rating][gte]'] = int(data['rating'])

    params = {
        'filter[screenshots][not_eq]': 'null',
        'filter[genres][not_eq]': 'null',
    }

    params.update(params_post)
    res = wrapper.get_games(params)

    games = []
    for game in res:
        games.append(Game(game['id']))

    paginator = Paginator(games, 8)    # object_list
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Set first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # Set last page, if the counter is bigger then max_page
        page_obj = paginator.page(paginator.num_pages)

    filter_panel = Filter()
    context = {
        'games': games,
        'filter_panel': filter_panel,
        'initials': initials,
        'page_obj': page_obj,
        'page_numbers': paginator.page_range
    }
    return render(request, 'board/main.html', context=context)


def detail(request, game_id):
    game = Game(game_id)
    context = {
        'game': game,
    }
    return render(request, 'board/detail.html', context=context)
