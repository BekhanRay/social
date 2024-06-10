from django.db import models


class Chat(models.Model):
    sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='receiver')


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



