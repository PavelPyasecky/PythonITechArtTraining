from django.test import TestCase
from django.urls import reverse

from board.models import Game


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
