from django.db import models
from uuid import uuid4


class Chat(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    initiator = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='initiator')
    receiver = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='receiver')

    # members = models.ManyToManyField('users.CustomUser')
    # def add_user(self, user):
    #     self.members.add(user)
    #     self.save()
    #
    # def remove_member(self, user):
    #     self.members.remove(user)

    def __str__(self):
        return str(self.uuid)


class Message(models.Model):
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='author')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='group')




