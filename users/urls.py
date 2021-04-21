from django.urls import path, re_path

from .views import SignUpView, account_activation, resend_auth_mail

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('reactivate/<slug:user_id>/', resend_auth_mail, name='reactivation'),
    path('activate/<slug:user_id>/', account_activation, name='activation'),
]