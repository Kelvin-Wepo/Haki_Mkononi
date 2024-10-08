import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import VideoCall

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'call_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        user_id = data['userId']

        if message_type == 'join':
            await self.update_call_status('ongoing')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'relay_message',
                'message_type': message_type,
                'user_id': user_id,
            }
        )

    async def relay_message(self, event):
        message_type = event['message_type']
        user_id = event['user_id']

        await self.send(text_data=json.dumps({
            'type': message_type,
            'userId': user_id,
        }))

    @database_sync_to_async
    def update_call_status(self, status):
        VideoCall.objects.filter(room_name=self.room_name).update(status=status)