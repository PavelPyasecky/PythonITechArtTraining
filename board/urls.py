from django.urls import path
from board import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:game_id>/detail/', views.detail, name='detail'),
    path('detail/', views.FavouriteView.as_view(), name='edit'),
    path('favourite/', views.get_user_favourite, name='favourite'),
]