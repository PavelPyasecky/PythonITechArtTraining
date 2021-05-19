from board.models import Game
from rest_framework import viewsets
from rest_framework import permissions
from board.serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Game.objects.all().order_by('-rating')[:3]
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
