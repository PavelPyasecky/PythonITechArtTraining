from django.urls import path
from .views import main, detail

urlpatterns = [
    path('', main, name='main'),
    path('<int:game_id>/detail/', detail, name='detail'),
]