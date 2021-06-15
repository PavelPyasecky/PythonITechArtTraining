from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from users.models import CustomUser


class SignUpViewTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.test_user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='testuser1@mail.ru',
            password='1X<ISRUkw+tuK',
            is_active=True
        )
        self.test_user1.save()

    def test_uses_correct_template(self):
        response = self.client.post(
            reverse('signup'),
            {'username': 'testuser2',
             'email': 'testuser2@mail.ru',
             'birthday': timezone.now(),
             'password1': '2HJ1vRV0Z&3iD',
             'password2': '2HJ1vRV0Z&3iD'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_HTTP404_for_invalid_username(self):
        response = self.client.post(
            reverse('signup'),
            {'username': 'testuser1',
             'email': 'testuser2@mail.ru',
             'birthday': timezone.now(),
             'password1': '1X<ISRUkw+tuK',
             'password2': '1X<ISRUkw+tuK'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    def test_HTTP404_for_invalid_email(self):
        response = self.client.post(
            reverse('signup'),
            {'username': 'testuser2',
             'email': 'testuser1@mail.ru',
             'birthday': timezone.now(),
             'password1': '1X<ISRUkw+tuK',
             'password2': '1X<ISRUkw+tuK'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'User with this Email address already exists.')

    def test_HTTP404_for_invalid_date(self):
        response = self.client.post(
            reverse('signup'),
            {'username': 'testuser2',
             'email': 'testuser2@mail.ru',
             'birthday': '01-01-2000',
             'password1': '1X<ISRUkw+tuK',
             'password2': '1X<ISRUkw+tuK'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'birthday', 'Enter a valid date.')

    def test_form_birthday_field_initially_has_date_today(self):
        response = self.client.get(reverse('signup'))
        field_birthday = response.context['form'].base_fields['birthday'].initial
        self.assertEqual(field_birthday, timezone.now)
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_password_confirmation(self):
        response = self.client.post(
            reverse('signup'),
            {'username': 'testuser2',
             'email': 'testuser2@mail.ru',
             'birthday': '01-01-2000',
             'password1': '1X<ISRUkw+tuK',
             'password2': '2HJ1vRV0Z&3iD'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
