from django.db import models
from django.conf import settings
from django.utils import timezone


class Chat(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_chats', on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_chats', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.DO_NOTHING)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender}: {self.content}"
