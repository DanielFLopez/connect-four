from django.urls import path

from .views import RegisterGame, CloseGames

app_name = 'api_game'

urlpatterns = [
    path('register/', RegisterGame.as_view()),
    path('close/', CloseGames.as_view())
]
