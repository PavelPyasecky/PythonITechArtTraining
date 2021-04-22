from users import views as users_views
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('signup/', users_views.SignUpView.as_view(), name='signup'),
    path('reactivate/<slug:user_id>/', users_views.resend_auth_mail, name='reactivation'),
    path('activate/<slug:user_id>/', users_views.account_activation, name='activation'),
    path('profile/', users_views.get_user_profile, name='profile'),
]