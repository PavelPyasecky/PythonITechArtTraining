from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.admin import widgets
from django.template.loader import render_to_string


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'birthday')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget = widgets.AdminDateWidget()

    def save(self):
        user = super().save()
        self._send_auth_mail(user)
        return user

    def _send_auth_mail(self, user):
        context = {
            'username': user.username,
            'activation_link': self._build_activation_link(user),
        }
        html_body = render_to_string('users/email.html', context)
        user.email_user('Account activation', 'Hello world!', html_message=html_body)

    @staticmethod
    def _build_activation_link(user):
        url = f'http://localhost:8000/users/activate/{user.password}'    # Production - https://
        print('Hash -> ', user.password)
        print('Activation link -> ', url)
        return url


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
