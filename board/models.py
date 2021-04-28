from django.db import models
from users.models import CustomUser


class Favourite(models.Model):
    game_id = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favourite_games')
