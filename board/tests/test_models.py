import uuid
from django.test import TestCase

from board.models import Favourite, Game, Genre, Platform, Image
from users.models import CustomUser


class FavouriteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = CustomUser.objects.create(id=1, username='user', is_active=True)
        Favourite.objects.create(game_id=1, user=user)

    def test_game_id_label(self):
        favourite = Favourite.objects.get(game_id=1)
        field_label = favourite._meta.get_field('game_id').verbose_name
        self.assertEqual(field_label, 'game id')

    def test_user_related_model(self):
        favourite = Favourite.objects.get(game_id=1)
        field_related_model = favourite._meta.get_field('user').related_model
        self.assertEqual(field_related_model.__name__, 'CustomUser')

    def test_user_db_constraint(self):
        favourite = Favourite.objects.get(game_id=1)
        field_db_constraint = favourite._meta.get_field('user').db_constraint
        self.assertEqual(field_db_constraint, True)

    def test_user_related_name(self):
        favourite = Favourite.objects.get(game_id=1)
        field_related_name = favourite._meta.get_field('user').related_query_name()
        self.assertEqual(field_related_name, 'favourite_games')


class GameModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Game.objects.create(id=1, name='First Game', slug='first-game',
                            full_description='Best game in the world!')

    def test_id_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_id_primary_key(self):
        game = Game.objects.get(id=1)
        field_primary_key = game._meta.get_field('id').primary_key
        self.assertEqual(field_primary_key, True)

    def test_name_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        game = Game.objects.get(id=1)
        field_max_length = game._meta.get_field('name').max_length
        self.assertEqual(field_max_length, 150)

    def test_name_unique(self):
        game = Game.objects.get(id=1)
        field_unique = game._meta.get_field('name').unique
        self.assertEqual(field_unique, True)

    def test_slug_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_slug_max_length(self):
        game = Game.objects.get(id=1)
        field_max_length = game._meta.get_field('slug').max_length
        self.assertEqual(field_max_length, 150)

    def test_slug_unique(self):
        game = Game.objects.get(id=1)
        field_unique = game._meta.get_field('slug').unique
        self.assertEqual(field_unique, True)

    def test_full_description_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('full_description').verbose_name
        self.assertEqual(field_label, 'full description')

    def test_release_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('release').verbose_name
        self.assertEqual(field_label, 'release')

    def test_release_default(self):
        game = Game.objects.get(id=1)
        field_default = game._meta.get_field('release').default
        self.assertEqual(field_default, None)

    def test_release_null(self):
        game = Game.objects.get(id=1)
        field_null = game._meta.get_field('release').null
        self.assertEqual(field_null, True)

    def test_rating_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('rating').verbose_name
        self.assertEqual(field_label, 'rating')

    def test_rating_null(self):
        game = Game.objects.get(id=1)
        field_null = game._meta.get_field('rating').null
        self.assertEqual(field_null, True)

    def test_rating_count_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('rating_count').verbose_name
        self.assertEqual(field_label, 'rating count')

    def test_rating_count_null(self):
        game = Game.objects.get(id=1)
        field_null = game._meta.get_field('rating_count').null
        self.assertEqual(field_null, True)

    def test_aggregated_rating_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('aggregated_rating').verbose_name
        self.assertEqual(field_label, 'aggregated rating')

    def test_aggregated_rating_null(self):
        game = Game.objects.get(id=1)
        field_null = game._meta.get_field('aggregated_rating').null
        self.assertEqual(field_null, True)

    def test_aggregated_rating_count_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('aggregated_rating_count').verbose_name
        self.assertEqual(field_label, 'aggregated rating count')

    def test_aggregated_rating_count_null(self):
        game = Game.objects.get(id=1)
        field_null = game._meta.get_field('aggregated_rating_count').null
        self.assertEqual(field_null, True)


class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        game = Game.objects.create(id=1, name='First Game', slug='first-game',
                                   full_description='Best game in the world!')
        Image.objects.create(url='https://www.python.org/static/img/python-logo.png',
                             game=game)

    def test_id_label(self):
        image = Image.objects.get(game__id=1)
        field_label = image._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_id_primary_key(self):
        image = Image.objects.get(game__id=1)
        field_primary_key = image._meta.get_field('id').primary_key
        self.assertEqual(field_primary_key, True)

    def test_id_default(self):
        image = Image.objects.get(game__id=1)
        field_default = image._meta.get_field('id').default
        self.assertEqual(field_default, uuid.uuid4)

    def test_id_editable(self):
        image = Image.objects.get(game__id=1)
        field_editable = image._meta.get_field('id').editable
        self.assertEqual(field_editable, False)

    def test_url_label(self):
        image = Image.objects.get(game__id=1)
        field_label = image._meta.get_field('url').verbose_name
        self.assertEqual(field_label, 'url')

    def test_url_max_length(self):
        image = Image.objects.get(game__id=1)
        field_max_length = image._meta.get_field('url').max_length
        self.assertEqual(field_max_length, 150)

    def test_url_unique(self):
        image = Image.objects.get(game__id=1)
        field_unique = image._meta.get_field('url').unique
        self.assertEqual(field_unique, True)

    def test_game_label(self):
        image = Image.objects.get(game__id=1)
        field_label = image._meta.get_field('game').verbose_name
        self.assertEqual(field_label, 'game')

    def test_game_related_model(self):
        image = Image.objects.get(game__id=1)
        field_related_model = image._meta.get_field('game').related_model
        self.assertEqual(field_related_model.__name__, 'Game')

    def test_game_on_delete(self):
        image = Image.objects.get(game__id=1)
        field_db_constraint = image._meta.get_field('game').db_constraint
        self.assertEqual(field_db_constraint, True)

    def test_game_related_name(self):
        image = Image.objects.get(game__id=1)
        field_related_name = image._meta.get_field('game').related_query_name()
        self.assertEqual(field_related_name, 'images')

    def test_is_cover_default(self):
        image = Image.objects.get(game__id=1)
        field_default = image._meta.get_field('is_cover').default
        self.assertEqual(field_default, False)


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        genre = Genre.objects.create(id=1, name='racing')
        genre.game.create(id=1, name='First Game', slug='first-game',
                          full_description='Best game in the world!')

    def test_id_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_id_primary_key(self):
        genre = Genre.objects.get(id=1)
        field_primary_key = genre._meta.get_field('id').primary_key
        self.assertEqual(field_primary_key, True)

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        field_max_length = genre._meta.get_field('name').max_length
        self.assertEqual(field_max_length, 150)

    def test_name_unique(self):
        genre = Genre.objects.get(id=1)
        field_unique = genre._meta.get_field('name').unique
        self.assertEqual(field_unique, True)

    def test_game_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('game').verbose_name
        self.assertEqual(field_label, 'game')

    def test_game_related_model(self):
        genre = Genre.objects.get(id=1)
        field_related_model = genre._meta.get_field('game').related_model
        self.assertEqual(field_related_model.__name__, 'Game')

    def test_game_related_name(self):
        genre = Genre.objects.get(id=1)
        field_related_name = genre._meta.get_field('game').related_query_name()
        self.assertEqual(field_related_name, 'genres')


class PlatformModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        platform = Platform.objects.create(id=1, name='windows')
        platform.game.create(id=1, name='First Game', slug='first-game',
                             full_description='Best game in the world!')

    def test_id_label(self):
        platform = Platform.objects.get(id=1)
        field_label = platform._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_id_primary_key(self):
        platform = Platform.objects.get(id=1)
        field_primary_key = platform._meta.get_field('id').primary_key
        self.assertEqual(field_primary_key, True)

    def test_name_label(self):
        platform = Platform.objects.get(id=1)
        field_label = platform._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        platform = Platform.objects.get(id=1)
        field_max_length = platform._meta.get_field('name').max_length
        self.assertEqual(field_max_length, 150)

    def test_name_unique(self):
        platform = Platform.objects.get(id=1)
        field_unique = platform._meta.get_field('name').unique
        self.assertEqual(field_unique, True)

    def test_game_label(self):
        platform = Platform.objects.get(id=1)
        field_label = platform._meta.get_field('game').verbose_name
        self.assertEqual(field_label, 'game')

    def test_game_related_model(self):
        platform = Platform.objects.get(id=1)
        field_related_model = platform._meta.get_field('game').related_model
        self.assertEqual(field_related_model.__name__, 'Game')

    def test_game_related_name(self):
        platform = Platform.objects.get(id=1)
        field_related_name = platform._meta.get_field('game').related_query_name()
        self.assertEqual(field_related_name, 'platforms')
