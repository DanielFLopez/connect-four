from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Game


class RegisterGame(APIView):
    def post(self, request, *args, **kwargs):

        user = request.data.get("user", None)
        type_game = int(request.data.get("type_game"))

        if user is None:
            return Response({'message': 'Bad request, no user'}, status=400)

        game = Game.objects.filter(status=Game.Status.PLAYING)

        if game.exists():
            return Response({'message': 'Sorry, there can only be one game at a time.'})

        game, created = Game.objects.get_or_create(status=Game.Status.WAITING)

        game.initilize_matrix()
        game.set_type_game(type_game)
        game.generate_posible_moves()

        if game.type_game == Game.Type.PVP:
            if created:
                game.set_player1(user)
                message = "Game created, waiting for other player"
            else:
                game.set_player2(user)
                game.start_game()
                message = "Game full"
        else:
            game.set_player1(user)
            game.set_player2("IA")
            game.start_game()
            message = "Ready"

        return Response({'message': message, 'game_id': game.id, 'type_game': game.type_game})


class CloseGames(APIView):

    def post(self, request, *args, **kwargs):
        Game.objects.exclude(status=Game.Status.FINALIZED).update(status=Game.Status.FINALIZED)
        return Response({'message': 'All games are closed'})
