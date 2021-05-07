import gamestore.settings as settings
import json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from board.tasks import update_or_download_game
from .api import igdbapi, twitterapi
from .logic.game import GameAPI, Game
from .logic.tweet import Tweet, TweetAPI
from django.http import HttpResponse
from django.views import View
from .models import Game as GameModel

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


class BaseGameView:
    def __init__(self, user):
        self.user = user

    def _get_context(self, game_id, is_favourite):
        if Game.is_exist(game_id):
            game = Game(game_id)
            tweets = Tweet.get_tweets(game_id)
        else:
            game = GameAPI(game_id)
            tweet_ids = twitter_wrapper.get_tweets_by_string(game.slug)
            if tweet_ids:
                tweets = [TweetAPI(tweet_id) for tweet_id in tweet_ids]
            else:
                tweets = None

        context = {
            'game': game,
            'tweets': tweets,
            'user': self.user,
            'is_favourite': is_favourite
        }
        return context


class DetailView(BaseGameView):
    def get_detail(self, game_id):
        is_favourite = False
        if self.user.is_authenticated:
            is_favourite = bool(self.user.favourite_games.filter(game_id=game_id).first())
        context = self._get_context(game_id, is_favourite)
        return context


class FavouriteView(View):
    def _data_init(self):
        data = json.loads(self.request.body.decode())
        self.game_id = data['game_id']
        self.favourite_games = self.request.user.favourite_games

    def post(self, request, *args, **kwargs):
        self._data_init()
        request.user.favourite_games.update_or_create(game_id=self.game_id, user=request.user)
        return HttpResponse(status=200)

    def delete(self, request, *args, **kwargs):
        self._data_init()
        favourite_game = request.user.favourite_games.filter(game_id=self.game_id).first()
        if favourite_game:
            favourite_game.delete()
        return HttpResponse(status=200)


def main(request):
    data = request.GET
    platforms = [item for item in data.getlist('platforms')]
    genres = [item for item in data.getlist('genres')]
    rating = data.get('rating', default=None)

    if rating:
        rating = int(rating)
    games = Game.get_games(platforms=platforms, genres=genres, rating=rating)
    if games:
        print('Games are here, in DB!!!')
    if not games:
        print('There are no games in DB!')
        print(platforms, genres, rating)
        res = igdb_wrapper.get_games(platforms=platforms, genres=genres, rating=[rating,])
        games = []
        if res:
            for game in res:
                update_or_download_game.delay(game['id'])
                games.append(GameAPI(game['id']))

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
    user = request.user
    detail_game = DetailView(user)
    context = detail_game.get_detail(game_id)
    return render(request, 'board/detail.html', context=context)


def get_user_favourite(request):
    game_list = [Game(item.game_id) for item in request.user.favourite_games.all()]
    context = {
        'games': game_list,
    }
    return render(request, 'board/favourite.html', context)
