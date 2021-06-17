from celery import shared_task
from django.core import management
from board.models import Favourite


@shared_task
def update_favourites(limit=None):
    favourites = Favourite.objects.all()
    if limit:
        favourites = favourites[:limit]
    for game in favourites:
        management.call_command('getgamefromapi', id=game.id)
