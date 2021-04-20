from django.urls import path, re_path

from .views import SignUpView, account_activation, resend_auth_mail

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:user_id>/', resend_auth_mail, name='reactivation'),
    path('activate/<slug:user_id>/<str:active_link_time>/', account_activation, name='activation'),
    # re_path(r'^activate/(?P<user_id>.*)/(?P<active_link_time>.*)', account_activation, name='activation'),
    # path('', profile, name='profile'),
]