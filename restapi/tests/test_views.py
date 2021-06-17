import json
from django.test import TestCase
from django.utils import timezone

from users.models import CustomUser
from board.models import Game, Image, Favourite, Genre, Platform


class UserViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = CustomUser.objects.create_user(
            id=1,
            username='testuser1',
            email='testuser1@mail.ru',
            birthday='2001-01-01',
            password='1X<ISRUkw+tuK',
            is_staff=False,
            last_login=timezone.now(),
            is_active=True
        )
        test_user2 = CustomUser.objects.create_user(
            id=2,
            username='testuser2',
            email='testuser2@mail.ru',
            birthday='2002-02-02',
            password='2HJ1vRV0Z&3iD',
            is_staff=False,
            last_login=timezone.now(),
            is_active=True
        )

        test_user1.save()
        test_user2.save()

    def test_get_api_users(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/api/users/')
        test_user1 = CustomUser.objects.get(id=1)
        data = {
            'id': 1,
            'username': 'testuser1',
            'email': 'testuser1@mail.ru',
            'birthday': '2001-01-01',
            'is_staff': False,
            'last_login': test_user1.last_login.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'][0], data)

    def test_get_api_users_by_id_1(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/api/users/1/')
        test_user1 = CustomUser.objects.get(id=1)
        data = {
            'id': 1,
            'username': 'testuser1',
            'email': 'testuser1@mail.ru',
            'birthday': '2001-01-01',
            'is_staff': False,
            'last_login': test_user1.last_login.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), data)

    def test_put_api_users_by_id_1_change_id(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'id': 99,
            'username': 'testuser1',
        }
        response = self.client.put('/api/users/1/', data=json.dumps(data),
                                   content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(json.loads(response.content)['id'], 99)

    def test_put_api_users_by_id_1_change_username(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'username': 'testuser1_new_username',
        }
        response = self.client.put('/api/users/1/', data=json.dumps(data),
                                   content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['username'], 'testuser1_new_username')

    def test_put_api_users_by_id_1_change_email(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'username': 'testuser1',
            'email': 'testuser1_new_email@mail.ru',
        }
        response = self.client.put('/api/users/1/', data=json.dumps(data),
                                   content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['email'], 'testuser1_new_email@mail.ru')

    def test_put_api_users_by_id_1_change_birthday(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'username': 'testuser1',
            'birthday': '2099-12-30'
        }
        response = self.client.put('/api/users/1/', data=json.dumps(data),
                                   content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['birthday'], '2099-12-30')

    def test_put_api_users_by_id_1_change_is_staff(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'username': 'testuser1',
            'is_staff': True,
        }
        response = self.client.put('/api/users/1/', data=json.dumps(data),
                                   content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_staff'], False)

    def test_put_api_users_by_id_1_change_last_login(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        last_login_new = timezone.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data = {
            'username': 'testuser1',
            'last_login': last_login_new
        }
        response = self.client.put('/api/users/1/', data=json.dumps(data),
                                   content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(json.loads(response.content)['last_login'], last_login_new)

    def test_post_api_users(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {
            'id': 1,
            'username': 'testuser3',
            'email': 'testuser3@mail.ru',
            'birthday': '2001-01-01',
            'is_staff': False,
        }
        response = self.client.post('/api/users/', data=json.dumps(data),
                                    content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(json.loads(response.content)['detail'], 'Method "POST" not allowed.')

    def test_delete_api_users(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.delete('/api/users/1/')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(json.loads(response.content)['detail'], 'Method "DELETE" not allowed.')


class GameViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user3 = CustomUser.objects.create_user(
            id=3,
            username='testuser3',
            email='testuser3@mail.ru',
            birthday='2003-03-03',
            password='3X<ISRUkw+tuK',
            is_staff=False,
            is_active=True
        )
        test_user_is_staff = CustomUser.objects.create_user(
            id=4,
            username='testuser_is_staff',
            email='testuser_is_staff@mail.ru',
            birthday='2004-04-04',
            password='SX<ISRUkw+tuK',
            is_staff=True,
            is_active=True
        )
        test_user3.save()
        test_user_is_staff.save()

        game = Game.objects.create(id=1, name='First Game', slug='first-game',
                                   full_description='Best game in the world!')
        genre = Genre.objects.create(id=1, name='racing')
        platform = Platform.objects.create(id=1, name='windows')
        genre.game.add(game)
        platform.game.add(game)
        Image.objects.create(url='https://www.python.org/static/img/python-logo.png',
                             game=game)
        Favourite.objects.create(game_id=1, user=test_user3)

    def test_get_api_games(self):
        login = self.client.login(username='testuser3', password='3X<ISRUkw+tuK')
        response = self.client.get('/api/games/')
        data = {
            'id': 1,
            'name': 'First Game',
            'slug': 'first-game',
            'genres': [1],
            'platforms': [1],
            'full_description': 'Best game in the world!',
            'release': None,
            'rating': None,
            'rating_count': None,
            'aggregated_rating': None,
            'aggregated_rating_count': None,
            'images': ['https://www.python.org/static/img/python-logo.png']
        }
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'][0], data)

    def test_get_api_games_by_id(self):
        login = self.client.login(username='testuser3', password='3X<ISRUkw+tuK')
        response = self.client.get('/api/games/1/')
        data = {
            'id': 1,
            'name': 'First Game',
            'slug': 'first-game',
            'genres': [1],
            'platforms': [1],
            'full_description': 'Best game in the world!',
            'release': None,
            'rating': None,
            'rating_count': None,
            'aggregated_rating': None,
            'aggregated_rating_count': None,
            'images': ['https://www.python.org/static/img/python-logo.png']
        }
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), data)

    def test_put_api_games_HTTP403_if_is_not_staff(self):
        login = self.client.login(username='testuser3', password='3X<ISRUkw+tuK')
        data = {
            'id': 1,
            'name': 'First Game New Name',
            'slug': 'first-game-new-name',
            'genres': [1],
            'platforms': [1],
            'full_description': 'Best game in the world! And in the universe',
            'release': None,
            'rating': None,
            'rating_count': None,
            'aggregated_rating': None,
            'aggregated_rating_count': None,
            'images': ['https://www.python.org/static/img/python-logo.png']
        }
        response = self.client.put('/api/games/1/', json.dumps(data),
                                   content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'],
                         'You do not have permission to perform this action.')

    def test_put_api_games_if_is_staff(self):
        login = self.client.login(username='testuser_is_staff', password='SX<ISRUkw+tuK')
        data = {
            'id': 1,
            'name': 'First Game New Name',
            'slug': 'first-game-new-name',
            'genres': [1],
            'platforms': [1],
            'full_description': 'Best game in the world! And in the universe',
            'release': None,
            'rating': None,
            'rating_count': None,
            'aggregated_rating': None,
            'aggregated_rating_count': None,
            'images': ['https://www.python.org/static/img/python-logo.png']
        }
        response = self.client.put('/api/games/1/', json.dumps(data),
                                    content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), data)

    def test_post_api_games_HTTP403_if_is_not_staff(self):
        login = self.client.login(username='testuser3', password='3X<ISRUkw+tuK')
        data = {
            'id': 2,
            'name': 'Second Game',
            'slug': 'second-game',
            'genres': [1],
            'platforms': [1],
            'full_description': 'Best game in the world too! And in the universe',
            'release': None,
            'rating': None,
            'rating_count': None,
            'aggregated_rating': None,
            'aggregated_rating_count': None,
            'images': []
        }
        response = self.client.post('/api/games/', json.dumps(data),
                                    content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'],
                         'You do not have permission to perform this action.')

    def test_post_api_games_if_is_staff(self):
        login = self.client.login(username='testuser_is_staff', password='SX<ISRUkw+tuK')
        data = {
            'id': 2,
            'name': 'Second Game',
            'slug': 'second-game',
            'genres': [1],
            'platforms': [1],
            'full_description': 'Best game in the world too! And in the universe',
            'release': None,
            'rating': None,
            'rating_count': None,
            'aggregated_rating': None,
            'aggregated_rating_count': None,
            'images': []
        }
        response = self.client.post('/api/games/', json.dumps(data),
                                    content_type='application/json')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), data)

    def test_delete_api_games_HTTP403_if_is_not_staff(self):
        login = self.client.login(username='testuser3', password='3X<ISRUkw+tuK')
        response = self.client.delete('/api/games/1/')
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['detail'],
                         'You do not have permission to perform this action.')

    def test_delete_api_games_if_is_staff(self):
        login = self.client.login(username='testuser_is_staff', password='SX<ISRUkw+tuK')
        response = self.client.delete('/api/games/1/')
        game_removed = Game.objects.filter(id=1).first()
        # Check our user is logged in
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(game_removed, None)
