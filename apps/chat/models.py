from apps.users.models import CustomUser as User
from django.db import models


class Chat(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatSender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatReceiver')

    def __str__(self):
        return self.room_name

    def absolute_url(self, path):
        return self.context['request'].build_absolute_uri(path)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messageSender')
    message = models.CharField(max_length=255, verbose_name='message')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message