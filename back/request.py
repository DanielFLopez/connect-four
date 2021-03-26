import json
import websocket

ws = websocket.WebSocket()

ws.connect('ws://0.0.0.0:8000/ws/game')

for i in range(1000):
    ws.send(json.dumps({'value': 0}))
