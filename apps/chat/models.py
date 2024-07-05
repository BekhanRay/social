from datetime import timedelta

from django.utils import timezone

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
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messageSender')
    message = models.CharField(max_length=255, verbose_name='message')
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_message_time(self):
        now = timezone.now()
        diff = now - self.timestamp

        if diff < timedelta(minutes=1):
            return f"{int(diff.total_seconds())} секунд назад"
        elif diff < timedelta(hours=1):
            return f"{int(diff.total_seconds() // 60)} минут назад"
        elif diff < timedelta(days=1):
            return f"{int(diff.total_seconds() // 3600)} часов назад"
        elif diff < timedelta(days=30):
            return f"{diff.days} дней назад"
        elif diff < timedelta(days=365):
            months = diff.days // 30
            return f"{months} месяцев назад"
        else:
            years = diff.days // 365
            return f"{years} лет назад"

    def __str__(self):
        return self.message