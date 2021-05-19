from django.urls import path, include
from rest_framework import routers
from board import api_views
from board import views


router = routers.DefaultRouter()
router.register(r'games', api_views.GameViewSet)


urlpatterns = [
    path('games/<int:game_id>/', api_views.GameItemView.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', views.MainView.as_view(), name='main'),
    path('<int:game_id>/detail/', views.DetailView.as_view(), name='detail'),
    path('detail/', views.FavouriteView.as_view(), name='edit'),
    path('favourite/', views.GetFavouriteView.as_view(), name='favourite'),
]
