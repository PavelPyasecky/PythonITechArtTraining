from django.urls import path, include
from rest_framework import routers
from restapi import views


router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'platforms', views.PlatformViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
