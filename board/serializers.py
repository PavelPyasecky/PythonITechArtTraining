from rest_framework import serializers
from board.models import Game, Genre, Image


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['name', 'slug', 'full_description',
                  'release', 'rating', 'rating_count',
                  'aggregated_rating', 'aggregated_rating_count', 'images',
                  'genres', 'platforms']

