from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()

@login_required
def get_chat(request, room_name):
    if request.method == "GET":
        chat = get_object_or_404(Chat, room_name=room_name)
        messages = Message.objects.filter(chat=chat)
        return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages})

    elif request.method == "POST":
        chat = get_object_or_404(Chat, room_name=room_name)
        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            message=request.POST['message'],
        )
        message.save()
        messages = Message.objects.filter(chat=chat)
        return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages})

@login_required
def create_chat(request, username):
    current_user = request.user
    other_user = get_object_or_404(User, login=username)

    if current_user.id > other_user.id:
        room_name = f'{current_user.id}_{other_user.id}'
    else:
        room_name = f'{other_user.id}_{current_user.id}'

    chat, created = Chat.objects.get_or_create(
        room_name=room_name,
        defaults={'sender': current_user, 'receiver': other_user}
    )

    return redirect('get_chat', room_name=room_name)

@login_required
def chat_view(request):
    if request.method == "GET":
        chats = Chat.objects.filter(sender=request.user).order_by('-id')
        return render(request, 'chat/chat_list.html', {'chats': chats})
