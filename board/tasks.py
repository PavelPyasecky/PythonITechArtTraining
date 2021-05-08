from celery import shared_task
from django.core import management
from board.models import Favourite


@shared_task
def update_or_download_game(game_id):
    management.call_command('getgamefromapi', id=game_id)


@shared_task
def update_favourites(slice=None):
    favourites = Favourite.objects.all()
    if slice:
        favourites = favourites[:slice]
    for game in favourites:
        management.call_command('getgamefromapi', id=game.id)
