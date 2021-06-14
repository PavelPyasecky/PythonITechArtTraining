from django.utils import timezone
from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        CustomUser.objects.create(id=1, username='user', is_active=True)

    def test_email_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email address')

    def test_email_unique(self):
        user = CustomUser.objects.get(id=1)
        field_unique = user._meta.get_field('email').unique
        self.assertEqual(field_unique, True)

    def test_email_blank(self):
        user = CustomUser.objects.get(id=1)
        field_blank = user._meta.get_field('email').blank
        self.assertEqual(field_blank, True)

    def test_birthday_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('birthday').verbose_name
        self.assertEqual(field_label, '%m/%d/%y')

    def test_birthday_default(self):
        user = CustomUser.objects.get(id=1)
        field_default = user._meta.get_field('birthday').default
        self.assertEqual(field_default, timezone.now)

    def test_is_active_default(self):
        user = CustomUser.objects.get(id=1)
        field_default = user._meta.get_field('is_active').default
        self.assertEqual(field_default, False)

    def test_activate_time_default(self):
        user = CustomUser.objects.get(id=1)
        field_default = user._meta.get_field('activate_time').default
        self.assertEqual(field_default, None)

    def test_activate_time_null(self):
        user = CustomUser.objects.get(id=1)
        field_null = user._meta.get_field('activate_time').null
        self.assertEqual(field_null, True)

    def test_activation_link_time_default(self):
        user = CustomUser.objects.get(id=1)
        field_default = user._meta.get_field('activation_link_time').default
        self.assertEqual(field_default, None)

    def test_activation_link_time_null(self):
        user = CustomUser.objects.get(id=1)
        field_null = user._meta.get_field('activation_link_time').null
        self.assertEqual(field_null, True)
