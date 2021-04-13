import datetime
import gamestore.settings as settings
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .apiwrappers import TwitterWrapper, IgdbWrapper


twitter_wrapper = TwitterWrapper(settings.API_TWITTER_TOKEN)
igdb_wrapper = IgdbWrapper(settings.API_IGDB_CLIENT_ID, settings.API_IGDB_TOKEN)


class Game:
    def __init__(self, game_id):

        res = igdb_wrapper.get_game_by_id(game_id)[0]

        self.id = game_id
        self.name = res['name']
        self.full_description = res['summary']
        if 'cover' in res:
            self.img_url = igdb_wrapper.get_img_url(res['cover']['image_id'], size='cover_big')
        else:
            self.img_url = igdb_wrapper.get_img_url(res['screenshots'][0]['image_id'], size='cover_big')
        if 'release_dates' in res:
            self.release = datetime.datetime.fromtimestamp(res['release_dates'][0])
        else:
            self.release = None
        self.screen_url = [igdb_wrapper.get_img_url(item['image_id']) for item in res['screenshots']]
        self.genres = [genre['name'] for genre in res['genres']]
        self.platforms = [platform['name'] for platform in res['platforms']] if res.get('platforms') else None
        if 'rating' in res:
            self.rating = [res['rating'], res['rating_count']]
        else:
            self.rating = ['', 0]
        if 'aggregated_rating' in res:
            self.aggregated_rating = [res['aggregated_rating'], res['aggregated_rating_count']]
        else:
            self.aggregated_rating = ['', 0]

        self.slug = res['slug']

        self.tweets = None


class Tweet:
    def __init__(self, tweet_id):
        tweet = twitter_wrapper.get_tweet_by_id(tweet_id)
        self.id = tweet['id']
        self.text = tweet['text']
        self.created_at = tweet['created_at']
        self.author_id = tweet['author_id']
        user = twitter_wrapper.get_user_by_id(self.author_id)
        self.author_name = user['username']
        self.author_url = user['url']


class Filter:
    def __init__(self):
        params = {
            'fields': 'name'
        }
        res_genres = igdb_wrapper.get_genres(params)
        res_platforms = igdb_wrapper.get_platforms(params)

        self.genres = res_genres
        if res_genres:
            self.genres.insert(0, {'id': 0, 'name': 'Any'})
        self.platforms = res_platforms


def main(request):
    data = request.GET

    platforms = [int(item) for item in data.getlist('platforms')]
    genres = [int(item) for item in data.getlist('genres')]
    rating = [int(item) for item in data.getlist('rating')]
    print(platforms, genres, rating)
    res = igdb_wrapper.get_games(platforms=platforms, genres=genres, rating=rating)

    games = []
    if res:
        for game in res:
            games.append(Game(game['id']))

    paginator = Paginator(games, 8)    # object_list
    page_number = data.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Set first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # Set last page, if the counter is bigger then max_page
        page_obj = paginator.page(paginator.num_pages)

    filter_panel = Filter()
    filter_initials = {
        'platforms': platforms,
        'genres': genres,
        'rating': rating
    }
    context = {
        'games': games,
        'filter_panel': filter_panel,
        'filter_initials': filter_initials,
        'page_obj': page_obj,
        'page_numbers': paginator.page_range
    }
    return render(request, 'board/main.html', context=context)


def detail(request, game_id):
    game = Game(game_id)
    tweets_id = twitter_wrapper.get_tweets_by_string(game.slug)
    if tweets_id:
        game.tweets = []
        for tweet_id in tweets_id[:8]:
            game.tweets.append(Tweet(tweet_id))
    context = {
        'game': game,
    }
    return render(request, 'board/detail.html', context=context)
