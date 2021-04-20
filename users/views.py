from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .models import CustomUser


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        super().form_valid(form)
        return render(self.request, 'registration/login.html', context={'nextstep': True})  # In progress ----------


def account_activation(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if user:
        user.is_active = True
        user.save()
    return render(request, 'users/activation.html')
