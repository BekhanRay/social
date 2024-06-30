import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.chat.models import Chat, Message
from apps.users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['user'].id
        self.room_name = self.scope['url_route']['kwargs']['id']
        if str(self.room_name).split('_')[0] != self.sender:
            self.receiver = str(self.room_name).split('_')[0]
        else:
            self.receiver = str(self.room_name).split('_')[1]
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

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        print('receive')

        await self.save_message(sender=self.sender, message=message, room_name=self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.sender,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'sender': sender,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, room_name, sender, message):
        sender = CustomUser.objects.get(id=sender)
        print(f'save_message_{sender}')
        print(room_name)
        chat = Chat.objects.get(room_name=room_name)
        message = Message.objects.create(chat=chat, sender=sender, message=message)
        message.save()

    async def get_messages(self, room_name):
        chat = Chat.objacts.get(room_name=room_name)
        messages = Message.objects.filter(chat=chat)
        return messages


