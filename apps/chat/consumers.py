# import json
#
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Chat, Message
# # from users.models import CustomUser
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         self.chat = await self.get_chat(self.room_name)
#         if self.chat and self.scope['user'] in self.chat.participants.all():
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             await self.accept()
#         else:
#             await self.close()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         sender = self.scope['user']
#
#         if self.chat and sender in self.chat.participants.all():
#             await self.save_message(sender, message)
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_message',
#                     'message': message,
#                     'sender': sender.username
#                 }
#             )
#
#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']
#
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender
#         }))
#
#     @database_sync_to_async
#     def get_chat(self, room_name):
#         try:
#             return Chat.objects.get(id=room_name)
#         except Chat.DoesNotExist:
#             return None
#
#     @database_sync_to_async
#     def save_message(self, sender, message):
#         Message.objects.create(
#             chat=self.chat,
#             sender=sender,
#             content=message
#         )
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        sender = await self.get_user(sender_id)
        chat = await self.get_chat(self.chat_id)

        if sender and chat:
            await self.create_message(chat, sender, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_chat(self, chat_id):
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def create_message(self, chat, sender, content):
        return Message.objects.create(chat=chat, sender=sender, content=content)
