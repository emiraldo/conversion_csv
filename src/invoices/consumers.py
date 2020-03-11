from datetime import date

from channels.generic.websocket import AsyncWebsocketConsumer
import json



class UploadCSVConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['token']
        self.room_group_name = '%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("se conecta")

        # today = date.today()
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'send_message',
        #         'message': str(today)
        #     }
        # )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass

    # Receive message from room group
    async def send_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
