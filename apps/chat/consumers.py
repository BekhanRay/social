# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from django.core.files.base import ContentFile
# from apps.chat.serializers import MessageSerializer
# from .models import Conversation, Message
# from asgiref.sync import sync_to_async
# from rest_framework_simplejwt.tokens import AccessToken
# from apps.users.models import Profile as User
# from .utils import *
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#
#     @sync_to_async
#     def get_user(self, user_id):
#         return User.objects.get(id=user_id)
#
#     @sync_to_async
#     def get_convo(self, convo_id):
#         return Conversation.objects.get(id=convo_id)
#
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         headers = dict(self.scope['headers'])
#         authorization_header = headers.get(b'authorization').decode('utf-8') if b'authorization' in headers else None
#
#         if authorization_header:
#             decoded_token = AccessToken(authorization_header)
#             user_id = decoded_token['user_id']
#             user = await self.get_user(user_id)
#         else:
#             await self.close()
#
#         convo = await self.get_convo(int(self.room_name))
#
#         @sync_to_async
#         def check_user():
#             return user == convo.initiator or user == convo.reciever
#
#         if await check_user():
#             await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#             await self.accept()
#         else:
#             await self.close()
#             return
#
#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(
#             self.room_group_name, self.channel_name
#         )
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         await self.channel_layer.group_send(
#             self.room_group_name, {'type': 'chat.message', 'message': message}
#         )
#
#     async def chat_message(self, event):
#         text_data_json = event.copy()
#         text_data_json.pop('type')
#
#         message = text_data_json['message']
#         conversation = await self.get_convo(int(self.room_name))
#
#         headers = dict(self.scope['headers'])
#         authorization_header = headers.get(b'authorization').decode('utf-8') if b'authorization' in headers else None
#
#         if authorization_header:
#             decoded_token = AccessToken(authorization_header)
#             user_id = decoded_token['user_id']
#             sender = await self.get_user(user_id)
#         else:
#             await self.close()
#
#         _message = await sync_to_async(Message.objects.create)(
#             sender=sender,
#             text=message,
#             conversation_id=conversation,
#         )
#
#         serializer = MessageSerializer(instance=_message)
#
#         await self.send(
#             text_data=json.dumps(
#                 serializer.data,
#                 ensure_ascii=False
#             )
#         )
#
#
# class UserConsumer(AsyncWebsocketConsumer):
#
#     @staticmethod
#     @sync_to_async
#     def find_user(token):
#         decoded_token = AccessToken(token)
#         user_instance = User.objects.get(id=decoded_token['user_id'])
#         return user_instance
#
#     async def connect(self):
#         token = self.scope['url_route']['kwargs']['token']
#         user = await self.find_user(token)
#         email = user.email
#         channel_name = self.channel_name
#         add_data_to_redis(email, channel_name)
#         await self.accept()
#
#     async def disconnect(self, code):
#         token = self.scope['url_route']['kwargs']['token']
#         user = await self.find_user(token)
#         email = user.email
#         remove_data_from_redis(email)
#
#     async def send_notification(self, event):
#         message = event["mesage"]
#
#         await self.send(
#             text_data=json.dumps(
#                 message, ensure_ascii=False
#             )
#         )
import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
from apps.users.models import CustomUser as User
from .models import Message, Chat


class ChatConsumer(WebsocketConsumer):

    @sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @sync_to_async
    def get_convo(self, convo_id):
        return Chat.objects.get(id=convo_id)

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['uuid']
        self.room_group_name = f'chat_{self.room_name}'

        @sync_to_async
        def check_user(self):
            user = self.get_user(self.scope['user'].id)
            return user == Chat.initiator or user == Chat.receiver

        if await check_user():
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()
            return

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat.message', 'message': message}
        )
