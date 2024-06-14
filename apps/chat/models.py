from django.db import models
from uuid import uuid4
from apps.users.models import CustomUser


class Chat(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='initiator')
    receiver = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return str(self.uuid)


class Message(models.Model):
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='author')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='group')




