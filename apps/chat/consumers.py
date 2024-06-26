import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        try:
            self.recipient = User.objects.get(username=self.scope['url_route']['kwargs']['username'])
            self.room_group_name = f'chat_{self.user.id}_{self.recipient.id}'

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        except ObjectDoesNotExist:
            self.close()

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error during disconnect: {e}")

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']

            chat_message = ChatMessage.objects.create(
                sender=self.user,
                recipient=self.recipient,
                message=message
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username
                }
            )
        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error during receive: {e}")
            self.send(text_data=json.dumps({
                'error': 'An error occurred'
            }))

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
