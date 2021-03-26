from django.urls import path, include

urlpatterns = [
    path('game/', include('game.urls', namespace='api_game_create')),
]
