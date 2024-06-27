import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from apps.chat.models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print('receive', text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = await self.get_user(self.room_name)

        await self.save_message(sender=sender, message=message, room_name=self.room_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': self.scope['user'],
                'message': message,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'sender': str(sender),
            'message': message
        }))


    @database_sync_to_async
    def get_user(self, login):
        return get_user_model().objects.filter(login=login).first()

    @database_sync_to_async
    def save_message(self, room_name, sender, message):
        print(sender)
        chat = Chat.objects.get(room_name=room_name)
        Message.objects.create(chat=chat, sender=sender, message=message)

    @database_sync_to_async
    def get_user(self, username):
        return get_user_model().objects.filter(login=username).first()