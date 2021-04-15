from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .models import CustomUser


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


def account_activation(request, user_hash):
    print('Hash: ', user_hash)
    user = CustomUser.objects.get(password=user_hash)
    print('User: ', user)
    error = False   # It is for debugging
    if user:
        user.is_active = True
        user.save()
        error = True
    return render(request, 'users/activation.html', context={'error': error})



