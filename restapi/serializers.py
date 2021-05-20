from rest_framework import serializers
from board.models import Game
from restapi import relations


class GameSerializer(serializers.HyperlinkedModelSerializer):
    genres = relations.GenreSerializer(many=True, read_only=True)
    platforms = relations.PlatformSerializer(many=True, read_only=True)
    images = relations.ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['name', 'slug', 'genres',
                  'platforms', 'full_description', 'release',
                  'rating', 'rating_count', 'aggregated_rating',
                  'aggregated_rating_count', 'images']
