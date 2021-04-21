from django.utils import timezone
from datetime import timedelta, datetime
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from .forms import CustomUserCreationForm
from gamestore.settings import ACCOUNT_ACTIVATION_URL


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        data_form = super().form_valid(form)
        form = AuthenticationForm(request=None)
        print(form.__dict__)
        return render(self.request, 'registration/login.html', context={'nextstep': True, 'form': form})


def account_activation(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    delta = timedelta(hours=3)
    difference = timezone.now() - user.link_time
    context = {
        'title': 'Something goes wrong...',
        'text': 'Your activation link has expired. Click on the button to create a new activation email.',
        'btn_name': 'create email',
        'btn_url_name': 'reactivation',
        'user': user,
    }
    if difference < delta:
        if user.is_active:
            context = {
                'title': 'DONE!',
                'text': 'Your account has already activated.',
                'btn_name': 'to site',
                'btn_url_name': 'main'
            }
        else:
            user.is_active = True
            user.activate_time = datetime.now()
            user.save()
            context = {
                'title': 'Congratulations!',
                'text': 'You have activated you account.',
                'btn_name': 'to site',
                'btn_url_name': 'main'
            }
    return render(request, 'users/activation.html', context=context)


def resend_auth_mail(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    now = datetime.now().timestamp()
    url = f'{ACCOUNT_ACTIVATION_URL}{user.id}/{now}'
    context = {
        'username': user.username,
        'activation_link': url,
    }
    html_body = render_to_string('users/email.html', context)
    user.email_user('Account activation', 'Confirmation', html_message=html_body)

    return render(request, 'registration/login.html', context={'nextstep': True})
