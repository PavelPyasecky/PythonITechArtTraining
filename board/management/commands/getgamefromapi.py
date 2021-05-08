import gamestore.settings as settings
from requests import get
from django.core.management.base import BaseCommand, CommandError
from board.models import Game, Image, Platforms, Genre
from board.logic.game import GameAPI
from board.api import igdbapi


igdb_wrapper = igdbapi.IgdbWrapper(settings.API_IGDB_CLIENT_ID, settings.API_IGDB_TOKEN)


class Command(BaseCommand):
    help = 'Add the specified filtered games to database'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--id', action='store', nargs='?', default=None, type=int)

    def handle(self, *args, **options):
        self._base_init()
        game_id = options['id']

        game = GameAPI(game_id)
        if game.is_empty():
            game = GameAPI(game_id)
            new_values = {
                'name': game.name,
                'slug': game.slug,
                'full_description': game.full_description,
                'release': game.release,
                'rating': game.rating[0],
                'rating_count': game.rating[1],
                'aggregated_rating': game.aggregated_rating[0],
                'aggregated_rating_count': game.aggregated_rating[1],
            }
            g1, created = Game.objects.update_or_create(id=game.id, defaults=new_values)

            Image.objects.update_or_create(url=game.img_url, defaults={'is_cover': True, 'game': g1})
            for i in range(len(game.screen_url)):
                Image.objects.update_or_create(url=game.screen_url[i], defaults={'game': g1})

            platforms = Platforms.objects.filter(name__in=game.platforms)
            genres = Genre.objects.filter(name__in=game.genres)
            for platform in platforms:
                g1.platforms.add(platform)
            for genre in genres:
                g1.genres.add(genre)

        else:
            raise CommandError('There is no game with such parameters')

        self.stdout.write(self.style.SUCCESS(f'Successfully added game with id: {game_id}'))

    @staticmethod
    def _download_img(url):
        response = get(url)
        response.raise_for_status()
        return response.content

    @staticmethod
    def _base_init():
        platforms = Platforms.objects.all()
        if platforms:
            return None
        params = {
            'fields': 'name'
        }
        platforms = igdb_wrapper.get_platforms(params)
        genres = igdb_wrapper.get_genres(params)
        [Platforms.objects.create(id=item['id'], name=item['name']) for item in platforms]
        [Genre.objects.create(id=item['id'], name=item['name']) for item in genres]
