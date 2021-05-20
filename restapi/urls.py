from django.urls import path, include
from rest_framework import routers
from restapi import views


router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)


urlpatterns = [
    path('games/<int:game_id>/', views.GameItemView.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
