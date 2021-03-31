import datetime
import requests
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


igdb_url = 'https://api.igdb.com/v4/'
igdb_headers = {'Client-ID': 'so25gzj451xajgpll19wm0badrh9sk',
                'Authorization': 'Bearer gd0r59g1nm5rem9j0bcj4ssmtrg4l8'}


class Game:
    def __init__(self, game_id):
        res = requests.post(igdb_url + 'games/', headers=igdb_headers, data='fields *;').json()[0]
        res_artwork = requests.post(igdb_url + 'artworks/', headers=igdb_headers, data='fields *;').json()[0]
        res_screenshots = requests.post(igdb_url + 'screenshots/', headers=igdb_headers,
                                        data='fields *; where game = {};'.format(game_id)).json()
        self.id = game_id
        self.name = res['name']
        self.desc_full = res['summary']
        if res_artwork:
            self.img_url = res_artwork['url']
        else:
            self.img_url = res_screenshots[0]['url']
        self.release = datetime.datetime.fromtimestamp(res['release_dates'][0])
        print(res_screenshots)
        self.screen_url = [item['url'] for item in res_screenshots]

    name = 'PACMAN'
    desc = 'arcade video game'
    img_url = 'static/board/img/pacman.jpg'
    desc_full = '''Pac-Man is a maze arcade game developed and released by Namco in 1980.
     The original Japanese title of Puck Man was changed to Pac-Man for international releases as a preventative 
     measure against defacement of the arcade machines by changing the P to an F. Outside Japan, the game was published
     by Midway Games as part of its licensing agreement with Namco America. The player controls Pac-Man, who must eat 
     all the dots inside an enclosed maze while avoiding four colored ghosts. Eating large flashing dots called 
     "Power Pellets" causes the ghosts to turn blue, allowing Pac-Man to eat them for bonus points. 
     '''
    release = 'Nov 1992'
    screen_url = ['../../static/board/img/screen1.png', '../../static/board/img/screen2.jpg',
                 '../../static/board/img/screen3.png',
                 '../../static/board/img/screen1.png', '../../static/board/img/screen2.jpg',
                 '../../static/board/img/screen3.png']
    genres = ['Arcade', 'Action']
    platforms = ['PC', 'PS4']
    rating = {'users': [7.32, 123], 'critics': [7.11, 123]}
    id = 1
    tweets = [['tweet_name', 'Pac-Man is a maze arcade game developed and released by Namco in 1980.'
                'The original Japanese title of Puck Man was changed to Pac-Man for international releases as '
                'a preventative',
               datetime.datetime.now()]] * 5


def main(request):
    games = [Game(70)] * 31

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

    context = {
        'games': games,
        'page_obj': page_obj,
        'page_numbers': paginator.page_range
    }
    return render(request, 'board/main.html', context=context)


def detail(request, game_id):
    games = [Game(70)] * 31
    context = {
        'game': games,
    }
    return render(request, 'board/detail.html', context=context)

