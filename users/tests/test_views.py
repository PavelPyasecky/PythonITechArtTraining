from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
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


class AccountActivationTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.test_user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='testuser1@mail.ru',
            password='1X<ISRUkw+tuK',
            activation_link_time=timezone.now() - timedelta(hours=1),
            is_active=False
        )
        self.test_user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='testuser2@mail.ru',
            password='2HJ1vRV0Z&3iD',
            activation_link_time=timezone.now() - timedelta(hours=4),
            is_active=False
        )
        self.test_user3 = CustomUser.objects.create_user(
            username='testuser3',
            email='testuser3@mail.ru',
            password='4tJ1X<ISR3iY',
            activation_link_time=timezone.now() - timedelta(hours=1),
            activate_time=timezone.now() - timedelta(hours=3),
            is_active=True
        )

        self.test_user1.save()
        self.test_user2.save()
        self.test_user3.save()

    def test_uses_correct_template(self):
        response = self.client.get(reverse('activation', kwargs={'user_id': self.test_user1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/activation.html')

    def test_user_account_activation(self):
        response = self.client.get(reverse('activation', kwargs={'user_id': self.test_user1.id}))
        test_user1 = CustomUser.objects.get(id=self.test_user1.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_user1.is_active, True)

    def test_user_account_activation_if_activation_link_is_false(self):
        response = self.client.get(reverse('activation', kwargs={'user_id': self.test_user2.id}))
        test_user2 = CustomUser.objects.get(id=self.test_user2.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_user2.is_active, False)

    def test_account_activation_message_if_activation_link_is_true(self):
        response = self.client.get(reverse('activation', kwargs={'user_id': self.test_user1.id}))
        message_title = response.context['title']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message_title, 'Congratulations!')

    def test_account_activation_message_if_activation_link_is_false(self):
        response = self.client.get(reverse('activation', kwargs={'user_id': self.test_user2.id}))
        message_title = response.context['title']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message_title, 'Something goes wrong...')

    def test_account_activation_message_if_account_is_activated(self):
        response = self.client.get(reverse('activation', kwargs={'user_id': self.test_user3.id}))
        message_title = response.context['title']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message_title, 'DONE!')
