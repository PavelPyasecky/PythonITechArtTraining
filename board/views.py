import gamestore.settings as settings
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .api import igdbapi, twitterapi
from .logic.game import Game
from .logic.tweet import Tweet


twitter_wrapper = twitterapi.TwitterWrapper(settings.API_TWITTER_TOKEN)
igdb_wrapper = igdbapi.IgdbWrapper(settings.API_IGDB_CLIENT_ID, settings.API_IGDB_TOKEN)


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
        'page_numbers': paginator.page_range,
        'user': request.user
    }
    return render(request, 'board/main.html', context=context)


def detail(request, game_id):
    game = Game(game_id)
    tweets = []
    tweets_id = twitter_wrapper.get_tweets_by_string(game.slug)
    if tweets_id:
        tweets = [Tweet(tweet) for tweet in tweets_id]
    context = {
        'game': game,
        'tweets': tweets,
        'user': request.user
    }
    return render(request, 'board/detail.html', context=context)
