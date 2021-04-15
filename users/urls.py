from django.urls import path, re_path
from .views import SignUpView, account_activation


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:user_hash>', account_activation, name='activation'),
    re_path(r'^activate/(?P<user_hash>.*)', account_activation, name='activation'),
    # path('', profile, name='profile'),
]