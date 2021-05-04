import datetime
import gamestore.settings as settings
from board.api import igdbapi
from django.utils.timezone import make_aware


igdb_wrapper = igdbapi.IgdbWrapper(settings.API_IGDB_CLIENT_ID, settings.API_IGDB_TOKEN)


class Game:
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
