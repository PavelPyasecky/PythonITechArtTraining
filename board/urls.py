from django.urls import path
from board import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:game_id>/detail/', views.detail, name='detail'),
    path('<int:game_id>/detail/add/', views.add_to_favourite, name='add'),
    path('<int:game_id>/detail/delete/', views.del_from_favourite, name='delete'),
    path('favourite/', views.get_user_favourite, name='favourite'),
]