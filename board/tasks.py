from celery import shared_task
from django.core import management
import gamestore.settings as settings
from board.api import igdbapi


igdb_wrapper = igdbapi.IgdbWrapper(settings.API_IGDB_CLIENT_ID, settings.API_IGDB_TOKEN)


@shared_task
def update_games(limit=10):
    offset = 0
    while True:
        response = igdb_wrapper.get_games(limit=limit, offset=offset)
        if not response:
            return
        for item in response:
            management.call_command('getgamefromapi', id=item['id'])
        offset = limit
        limit += limit
