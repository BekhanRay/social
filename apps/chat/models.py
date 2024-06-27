from apps.users.models import CustomUser as User
from django.db import models


class Chat(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatSender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatReceiver')

    def __str__(self):
        return f'{self.sender} -> {self.receiver}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messageSender')
    message = models.TextField(max_length=255, verbose_name='message')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender