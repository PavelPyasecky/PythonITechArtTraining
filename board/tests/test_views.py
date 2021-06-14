import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from board.models import Game
from users.models import CustomUser


class MainViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_games = 10

        for game_id in range(number_of_games):
            Game.objects.create(
                id=game_id,
                name=f'Super Game {game_id}',
                slug=f'super-game-{game_id}',
                rating=50,
                full_description='Best Game in the world!'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/main.html')

    def test_pagination(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_numbers' in response.context)
        self.assertEqual(response.context['page_obj'].paginator.per_page, 8)
        self.assertEqual(len(response.context['page_obj']), 8)

    def test_lists_all_games(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(reverse('main')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_numbers' in response.context)
        self.assertEqual(response.context['page_obj'].paginator.per_page, 8)
        self.assertEqual(len(response.context['page_obj']), 2)


class LoggedInUserViewsTest(TestCase):
    def setUp(self):
        # Create user
        test_user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='testuser1@mail.ru',
            password='1X<ISRUkw+tuK',
            is_active=True
        )
        test_user1.save()

        # Create a game
        Game.objects.create(
            id=1,
            name=f'Super Game 1',
            slug=f'super-game-1',
            rating=50,
            full_description='Best Game in the world!'
        )

    def test_logged_in_must_to_favourites(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {'game_id': 1}
        response = self.client.post(
            reverse('edit'),
            content_type='application/json',
            data=json.dumps(data))

        # Check our user is logged in
        self.assertEqual(login, True)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_logged_in_list_all_favourites(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {'game_id': 1}
        response_add_game = self.client.post(
            reverse('edit'),
            content_type='application/json',
            data=json.dumps(data))

        response = self.client.get(reverse('favourite'))

        self.assertEqual(response_add_game.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('games' in response.context)
        self.assertEqual(len(response.context['games']), 1)

    def test_logged_in_remove_from_favourites(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        data = {'game_id': 1}
        response_add_game = self.client.post(
            reverse('edit'),
            content_type='application/json',
            data=json.dumps(data))

        response_delete_game = self.client.delete(
            reverse('edit'),
            content_type='application/json',
            data=json.dumps(data))

        self.assertEqual(response_add_game.status_code, 200)
        # Check our user is logged in
        self.assertEqual(login, True)
        # Check that we got a response "success"
        self.assertEqual(response_delete_game.status_code, 200)
