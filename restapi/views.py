from board.models import Game, Genre, Platform
from users.models import CustomUser as User
from rest_framework import viewsets
from rest_framework import permissions
from restapi.permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly
from restapi import serializers
from rest_framework import mixins
from users.models import CustomUser
from users.views import resend_auth_mail


class GameViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Game.objects.all().order_by('-rating')
    serializer_class = serializers.GameSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsStaffOrReadOnly]


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Platform.objects.all()
    serializer_class = serializers.PlatformSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(mixins.UpdateModelMixin,
                  viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `retrieve` and `update` actions.
    """
    queryset = User.objects.order_by('-last_login')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code != 200:
            return response
        user = CustomUser.objects.get(id=kwargs['pk'])
        user.is_active = False
        user.save()
        resend_auth_mail(request, user_id=kwargs['pk'])
        return response
