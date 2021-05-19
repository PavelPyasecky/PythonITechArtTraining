from board.models import Game
from rest_framework import viewsets
from rest_framework import permissions
from board.serializers import GameSerializer
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
        if not game_id:
            return Response({'error': 'There is no game with such id!'})
        game = Game.objects.filter(id=game_id).first()
        serializer = GameSerializer(game)
        return Response(serializer.data)
