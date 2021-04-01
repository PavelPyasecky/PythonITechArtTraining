import datetime
import requests
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


igdb_url = 'https://api.igdb.com/v4/'
igdb_headers = {'Client-ID': 'so25gzj451xajgpll19wm0badrh9sk',
                'Authorization': 'Bearer gd0r59g1nm5rem9j0bcj4ssmtrg4l8'}


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

        res = requests.post(igdb_url + 'games/', headers=igdb_headers, params=params).json()[0]

        self.id = game_id
        self.name = res['name']
        self.desc = ' '.join([genre['name'] for genre in res['genres']])
        self.desc_full = res['summary']
        if 'cover' in res:
            self.img_url = get_img_url(res['cover']['image_id'])
        else:
            self.img_url = get_img_url(res['screenshots'][0]['image_id'])
        self.release = datetime.datetime.fromtimestamp(res['release_dates'][0])
        self.screen_url = [get_img_url(item['image_id']) for item in res['screenshots']]
        self.genres = [genre['name'] for genre in res['genres']]
        self.platforms = [platform['name'] for platform in res['platforms']]
        if 'rating' in res:
            self.rating = [res['rating'], res['rating_count']]
        else:
            self.rating = ['', 0]
        if 'aggregated_rating' in res:
            self.aggregated_rating = [res['aggregated_rating'], res['aggregated_rating_count']]
        else:
            self.aggregated_rating = ['', 0]

    tweets = [['tweet_name', 'Pac-Man is a maze arcade game developed and released by Namco in 1980.'
                'The original Japanese title of Puck Man was changed to Pac-Man for international releases as '
                'a preventative',
               datetime.datetime.now()]] * 5


class Filter:
    def __init__(self):
        params = {
            'fields': 'name'
        }

        res_genres = requests.post(igdb_url + 'genres/', headers=igdb_headers, params=params).json()
        res_platforms = requests.post(igdb_url + 'platforms/', headers=igdb_headers, params=params).json()

        self.genres = [item['name'] for item in res_genres]
        self.platforms = [item['name'] for item in res_platforms]



def main(request):
    params = {
        'filter[screenshots][not_eq]': 'null',
        'filter[genres][not_eq]': 'null'
    }
    res = requests.post(igdb_url + 'games/', headers=igdb_headers, params=params).json()
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

