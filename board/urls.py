from django.urls import path
from board import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:game_id>/detail/', views.GameDetailView.as_view(), name='detail'),
    path('detail/', views.FavouriteView.as_view(), name='edit'),
    path('favourite/', views.GetFavouriteView.as_view(), name='favourite'),
]