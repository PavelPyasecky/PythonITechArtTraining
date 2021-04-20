from datetime import timedelta, datetime
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import views
from .models import CustomUser
from .forms import CustomUserCreationForm
from gamestore.settings import ACCOUNT_ACTIVATION_URL


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    # TODO--------------
    def form_valid(self):
        self.object = self.get_form().save()
        return render(self.request, 'registration/login.html', context={'nextstep': True})

# TODO ----------------
class CustomLoginView(views.LoginView):

    def get(self):
        context = super().get_context_data()
        context['nextstep'] = False
        return self.render_to_response(context)


def account_activation(request, user_id, active_link_time):
    user = CustomUser.objects.get(id=user_id)
    delta = timedelta(hours=3)
    active_link_time = float(active_link_time)
    difference = datetime.now() - datetime.fromtimestamp(active_link_time)
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
