import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import sync_to_async
import requests



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"

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
        message = data['message']

        user = self.scope.get('user')

        sender_id = user.get('user_id') if user else "anonymous"
        sender_role = user.get('role') if user else "unknown"

        await save_message(self.room_id, sender_id, sender_role, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'sender_role': sender_role
            }
        )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_role': event['sender_role']
        }))

@sync_to_async
def save_message(room_id, sender_id, sender_role, content):
        Message.objects.create(
            room_id=room_id,
            sender_id=sender_id,
            sender_role=sender_role,
            content=content
        )
