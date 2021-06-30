from django.core.management.base import BaseCommand, CommandError

import gamestore.settings as settings
from board.api import igdbapi
from board.logic.game import GameAPI
from board.models import Game, Genre, Image, Platform

igdb_wrapper = igdbapi.IgdbWrapper(settings.API_IGDB_CLIENT_ID, settings.API_IGDB_TOKEN)


class Command(BaseCommand):
    help = "Add the specified filtered games to database"

    def add_arguments(self, parser):
        parser.add_argument(
            "-i", "--id", action="store", nargs="?", default=None, type=int
        )

    def handle(self, *args, **options):
        self._base_init()
        game_id = options["id"]

        game_api_response_object = GameAPI(game_id)
        if game_api_response_object.is_empty():
            new_values = {
                "name": game_api_response_object.name,
                "slug": game_api_response_object.slug,
                "full_description": game_api_response_object.full_description,
                "release": game_api_response_object.release,
                "rating": game_api_response_object.rating[0],
                "rating_count": game_api_response_object.rating[1],
                "aggregated_rating": game_api_response_object.aggregated_rating[0],
                "aggregated_rating_count": game_api_response_object.aggregated_rating[
                    1
                ],
            }
            game, created = Game.objects.update_or_create(
                id=game_api_response_object.id, defaults=new_values
            )

            Image.objects.update_or_create(
                url=game_api_response_object.img_url,
                defaults={"is_cover": True, "game": game},
            )
            for i in range(len(game_api_response_object.screen_url)):
                Image.objects.update_or_create(
                    url=game_api_response_object.screen_url[i], defaults={"game": game}
                )

            platforms = Platform.objects.filter(
                name__in=game_api_response_object.platforms
            )
            genres = Genre.objects.filter(name__in=game_api_response_object.genres)
            game.platforms.add(*platforms)
            game.genres.add(*genres)

        else:
            raise CommandError("There is no game with such parameters")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully added game with id: {game_id}")
        )

    @staticmethod
    def _base_init():
        params = {"fields": "name"}
        platforms_api = igdb_wrapper.get_platforms(params)
        genres_api = igdb_wrapper.get_genres(params)

        platforms = Platform.objects.all()
        genres = Genre.objects.all()

        for item in platforms_api:
            if item["id"] not in platforms:
                Platform.objects.update_or_create(id=item["id"], name=item["name"])

        for item in genres_api:
            if item["id"] not in genres:
                Genre.objects.update_or_create(id=item["id"], name=item["name"])
