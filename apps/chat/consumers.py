import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.chat.models import Chat, Message
from apps.users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['user'].id if self.scope['user'].is_authenticated else int(self.scope['query_string'].decode())
        self.receiver = self.scope['url_route']['kwargs']['id']
        self.room_name = (
            f'{self.sender}_{self.receiver}'
            if int(self.sender) > int(self.receiver)
            else f'{self.receiver}_{self.sender}'
        )
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
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.sender
        receiver = self.receiver

        await self.save_message(sender=sender, receiver=receiver, message=message, room_name=self.room_name)

        messages = await self.get_messages(self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'messages': [msg['message'] for msg in messages],
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        messages = event['messages']

        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'sender': sender,
                    'messages': messages,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, room_name, sender, receiver, message):
        sender_user = CustomUser.objects.get(id=sender)
        receiver_user = CustomUser.objects.get(id=receiver)
        chat, created = Chat.objects.get_or_create(room_name=room_name, sender=sender_user, receiver=receiver_user)
        Message.objects.create(chat=chat, sender=sender_user, message=message)

    @database_sync_to_async
    def get_messages(self, room_name):
        chat = Chat.objects.get(room_name=room_name)
        return list(Message.objects.filter(chat=chat).order_by('-timestamp').values('message'))
