import datetime
import gamestore.settings as settings
from board.api import igdbapi
from board.models import Game as GameModel
from django.utils.timezone import make_aware


igdb_wrapper = igdbapi.IgdbWrapper(settings.API_IGDB_CLIENT_ID, settings.API_IGDB_TOKEN)


class GameAPI:
    def __init__(self, game_id):
        res = igdb_wrapper.get_game_by_id(game_id)

        self.id = game_id
        self.name = res['name']
        self.full_description = res['summary']
        if 'cover' in res:
            self.img_url = igdb_wrapper.get_img_url(res['cover']['image_id'], size='cover_big')
        else:
            self.img_url = igdb_wrapper.get_img_url(res['screenshots'][0]['image_id'], size='cover_big')
        if 'release_dates' in res:
            self.release = make_aware(datetime.datetime.fromtimestamp(res['release_dates'][0]))
        else:
            self.release = None
        self.screen_url = [igdb_wrapper.get_img_url(item['image_id']) for item in res['screenshots']]
        self.genres = [genre['name'] for genre in res['genres']]
        self.platforms = [platform['name'] for platform in res['platforms']] if res.get('platforms') else None
        if 'rating' in res:
            self.rating = [res['rating'], res['rating_count']]
        else:
            self.rating = [None, 0]
        if 'aggregated_rating' in res:
            self.aggregated_rating = [res['aggregated_rating'], res['aggregated_rating_count']]
        else:
            self.aggregated_rating = [None, 0]
        self.slug = res['slug']


class Game:
    def __init__(self, game_id):
        game = GameModel.objects.get(id=game_id)

        self.id = game.id
        self.name = game.name
        self.slug = game.slug
        self.full_description = game.full_description
        img = game.images.filter(game=game_id, is_cover=True).first()
        if img:
            self.img_url = img.url
        else:
            self.img_url = None
        self.release = game.release
        self.screen_url = [item.url for item in game.images.filter(game=game_id, is_cover=False)]
        self.genres = [item.name for item in game.genres.filter(game=game_id)]
        self.platforms = [item.name for item in game.platforms.filter(game=game_id)]
        self.rating = [game.rating, game.rating_count]
        self.aggregated_rating = [game.aggregated_rating, game.aggregated_rating_count]

    @staticmethod
    def get_games(platforms, genres, rating):
        params = dict()
        if platforms:
            params['platforms__id__in'] = platforms
        if genres:
            params['genres__id__in'] = genres
        if rating:
            params['rating__gte'] = rating
        games = GameModel.objects.filter(**params)
        game_objects = [Game(game.id) for game in games]
        return game_objects
