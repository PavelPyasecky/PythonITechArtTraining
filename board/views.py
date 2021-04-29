import gamestore.settings as settings
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .api import igdbapi, twitterapi
from .logic.game import Game
from .logic.tweet import Tweet
from .models import Favourite
from django.contrib.sites.shortcuts import get_current_site


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
        game = Game(game_id)
        tweets = self._get_tweets(game.slug)
        context = {
            'game': game,
            'tweets': tweets,
            'user': self.user,
            'is_favourite': is_favourite
        }
        return context

    @staticmethod
    def _get_tweets(game_slug):
        tweets_id = twitter_wrapper.get_tweets_by_string(game_slug)
        if tweets_id:
            return [Tweet(tweet) for tweet in tweets_id]
        return None


class DetailView(BaseGameView):
    def get_detail(self, game_id):
        context = self._get_context(game_id, False)
        return context


class FavouriteView(BaseGameView):
    def __init__(self, user):
        super().__init__(user)
        self.favourite_games = self.user.favourite_games

    def add_to_favourite(self, game_id):
        Favourite.objects.create(game_id=game_id, user=self.user)
        context = self._get_context(game_id, True)
        return context

    def del_from_favourite(self, game_id, ref_page):
        favourite_game = Favourite.objects.filter(game_id=game_id).first()
        if favourite_game:
            favourite_game.delete()

        if 'detail' in ref_page:
            context = self._get_context(game_id, False)
        else:
            context = {
                'games': self.favourite_games,
            }
        return context


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
    user = request.user
    favourites = DetailView(user)
    context = favourites.get_detail(game_id)
    return render(request, 'board/detail.html', context=context)


def add_to_favourite(request, game_id):
    user = request.user
    favourites = FavouriteView(user)
    context = favourites.add_to_favourite(game_id)
    return render(request, 'board/detail.html', context=context)


def del_from_favourite(request, game_id):
    user = request.user
    favourites = FavouriteView(user)
    ref_page = request.META.get('HTTP_REFERER')
    context = favourites.del_from_favourite(game_id, ref_page)
    current_site = get_current_site(request)
    if 'detail' in ref_page:
        return render(request, 'board/detail.html', context=context)
    return redirect(f'http://{current_site}/favourite/', context=context)


def get_user_favourite(request):
    game_list = [Game(item.game_id) for item in request.user.favourite_games.all()]
    context = {
        'games': game_list,
    }
    return render(request, 'board/favourite.html', context)
