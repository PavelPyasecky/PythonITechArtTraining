from django.urls import path
from users import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('reactivate/<slug:user_id>/', views.resend_auth_mail, name='reactivation'),
    path('activate/<slug:user_id>/', views.account_activation, name='activation'),
    path('profile/', views.get_user_profile, name='profile'),
]