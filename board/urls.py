from django.urls import path
from board import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:game_id>/detail/', views.detail, name='detail'),
    path('<int:game_id>/detail/add/', views.add_to_favourite, name='add'),
    path('detail/add_js/', views.add_to_favourite_js, name='add_js'),
    path('detail/delete_js/', views.del_from_favourite_js, name='delete_js'),
    path('<int:game_id>/detail/delete/', views.del_from_favourite, name='delete'),
    path('favourite/', views.get_user_favourite, name='favourite'),
]