from celery import shared_task
from gamestore.celery import app
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


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(5.0, update_favourites.s(), name='add every 10m')
