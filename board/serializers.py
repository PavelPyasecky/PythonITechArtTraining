from rest_framework import serializers
from board.models import Game, Genre, Platform, Image


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['id']


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Platform
        fields = ['id']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['url']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['name', 'slug', 'genres',
                  'platforms', 'full_description', 'release',
                  'rating', 'rating_count', 'aggregated_rating',
                  'aggregated_rating_count', 'images']

