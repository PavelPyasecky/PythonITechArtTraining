from celery import shared_task
from django.core import management
from board.models import Favourite


@shared_task
def update_or_download_game(game_id):
    print('Now, I am inside task.')
    management.call_command('getgamefromapi', id=game_id)
    management.call_command('gettweetsfromapi', id=game_id)


@shared_task
def update_favourites(slice=None):
    print('Now, I am inside Favourite task.')
    favourites = Favourite.objects.all()
    if slice:
        favourites = favourites[:slice]
    for game in favourites:
        management.call_command('getgamefromapi', id=game.id)
        management.call_command('gettweetsfromapi', id=game.id)
