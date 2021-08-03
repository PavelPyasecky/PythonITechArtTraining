import datetime

from django.test import TestCase

from users.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserCreationFormTest(TestCase):
    def test_custom_user_creation_form_username_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_custom_user_creation_form_email_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields['email'].label == 'Email address')

    def test_custom_user_creation_form_birthday_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields['birthday'].label == '%m/%d/%y')

    def test_custom_user_creation_form_birthday_field_help_text(self):
        form = CustomUserCreationForm()
        self.assertEqual(form._meta.model.birthday.field.get_default().date(),
                         datetime.date.today())

    def test_custom_user_creation_form_password_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields['password1'].label == 'Password')

    def test_custom_user_creation_form_password_confirmation_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields['password2'].label == 'Password confirmation')


class CustomUserChangeFormTest(TestCase):
    def test_custom_user_creation_form_username_field_label(self):
        form = CustomUserChangeForm()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_custom_user_creation_form_email_field_label(self):
        form = CustomUserChangeForm()
        self.assertTrue(form.fields['email'].label == 'Email address')
