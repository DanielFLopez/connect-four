from asgiref.sync import async_to_sync

import json

from channels.generic.websocket import WebsocketConsumer

from game.models import Game
from game.controller import process_game


class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = "game"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        type_message = data['type_message']

        if type_message == 'initial':
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'game_turn',
                    'data': data
                }
            )

        if type_message == 'message':
            value = process_game(data['column'], data['row'], data['user'], data['game'])
            if value['is_winner']:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'set_winner',
                        'data': value
                    }
                )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'game_request',
                    'data': value
                }
            )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def game_request(self, event):
        data = event['data']
        data['type_message'] = 'message'
        self.send(text_data=json.dumps(data))

    def game_turn(self, event):
        data = event['data']
        game = Game.objects.get(pk=data['game'])
        if game.type_game == Game.Type.PVE:
            ready = True
        else:
            ready = game.is_full()
        self.send(text_data=json.dumps({'type_message': 'initial', 'turn': game.get_user_by_turn(), 'status': ready}))

    def set_winner(self, event):
        data = event['data']
        self.send(text_data=json.dumps({'type_message': 'winner', 'message': data['message'], 'matrix_value':  data['matrix_value']}))
