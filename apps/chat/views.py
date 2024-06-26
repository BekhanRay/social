from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from apps.users.models import CustomUser as User
from django.db.models import Q

class ChatMessageList(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user = self.request.user
        recipient = User.objects.get(username=self.kwargs['username'])
        return ChatMessage.objects.filter(
            Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
        ).order_by('timestamp')

class ChatMessageCreate(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

@login_required
def chat_view(request, username):
    recipient = get_object_or_404(User, login=username)
    return render(request, 'chat.html', {'recipient': recipient})