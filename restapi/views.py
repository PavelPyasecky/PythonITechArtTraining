from board.models import Game
from rest_framework import viewsets
from rest_framework import permissions
from restapi.serializers import GameSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by('-rating')[:3]
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]


class GameItemView(APIView):
    queryset = Game.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, game_id=None):
        game = Game.objects.filter(id=game_id).first()
        if not game:
            return Response({'error': 'There is no game with such id!'})
        serializer = GameSerializer(game)
        return Response(serializer.data)
