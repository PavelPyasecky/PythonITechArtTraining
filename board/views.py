import gamestore.settings as settings
import json
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from board.tasks import update_or_download_game
from .api import igdbapi, twitterapi
from .logic.game import GameAPI, Game
from .logic.tweet import Tweet
from django.http import HttpResponse
from django.views import View


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


class GameDetailView(View):
    def get(self, request, game_id):
        game = self._get_game(game_id)
        tweets = self._get_tweets(game.slug)

        is_favourite = self.request.user.favourite_games.filter(game_id=self.kwargs['game_id']).exists()
        context = {
            'game': game,
            'tweets': tweets,
            'is_favourite': is_favourite,
        }
        return render(request, 'board/detail.html', context=context)

    @staticmethod
    def _get_game(game_id):
        if Game.is_exist(game_id):
            game = Game(game_id)
        else:
            game = GameAPI(game_id)
        return game

    @staticmethod
    def _get_tweets(game_slug):
        tweet_ids = twitter_wrapper.get_tweets_by_string(game_slug)
        if tweet_ids:
            tweets = [Tweet(tweet_id) for tweet_id in tweet_ids]
        else:
            tweets = None
        return tweets


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


class GetFavouriteView(View):
    def get(self, request):
        game_list = [Game(item.game_id) for item in request.user.favourite_games.all()]
        context = {
            'games': game_list,
        }
        return render(request, 'board/favourite.html', context)


class MainView(View):
    def _data_init(self):
        data = self.request.GET
        self.platforms = [item for item in data.getlist('platforms')]
        self.genres = [item for item in data.getlist('genres')]
        self.rating = data.get('rating', default=50)

    def get(self, request):
        self._data_init()
        games = Game.get_games(platforms=self.platforms, genres=self.genres, rating=int(self.rating))

        if not games:
            response = igdb_wrapper.get_games(platforms=self.platforms, genres=self.genres, rating=[self.rating,])
            games = []
            if response:
                for game in response:
                    update_or_download_game.delay(game['id'])
                    games.append(GameAPI(game['id']))

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
        filter_initials = {
            'platforms': self.platforms,
            'genres': self.genres,
            'rating': int(self.rating)
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
