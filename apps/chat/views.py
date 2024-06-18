from django.shortcuts import render, get_object_or_404, redirect
from apps.users.models import CustomUser
from .models import Chat, Message
from .forms import MessageForm


def create_chat(request, receiver_id):
    receiver = get_object_or_404(CustomUser, id=receiver_id)
    chat, created = Chat.objects.get_or_create(participants__in=[request.user, receiver])

    if created:
        chat.participants.add(request.user, receiver)

    return redirect('chat_room', room_name=chat.id)


def chat_room(request, room_name):
    chat = get_object_or_404(Chat, id=room_name)
    if request.user not in chat.participants.all():
        return redirect('home')

    return render(request, 'messages/chat_room.html', {'room_name': room_name, 'chat': chat})

