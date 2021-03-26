import os
import django

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from game.consumer import GameConsumer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")
django.setup()


websocket_url = [
  path('ws/game', GameConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_url
            )
        )
})
