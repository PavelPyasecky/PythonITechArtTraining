from django.urls import path
from .views import main, detail

urlpatterns = [
    path('', main, name='main'),
    path('detail/', detail, name='detail'),
]