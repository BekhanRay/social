from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()

@login_required
def get_chat(request, room_name):
    print('get_chat')
    if request.method == "GET":
        chat = Chat.objects.get(room_name=room_name)
        messages = Message.objects.filter(chat=chat).order_by('-timestamp')
        # print(messages)
        return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages})

    elif request.method == "POST":
        sender = request.user
        if str(room_name).split('_')[0] != sender.id:
            receiver = str(room_name).split('_')[0]
        else:
            receiver = str(room_name).split('_')[1]
        receiver = User.objects.get(id=receiver)
        print(receiver, sender)
        chat = Chat.objects.get(room_name=room_name)
        message = Message.objects.create(
            chat=chat,
            sender=receiver,
            message=request.POST['message'],
        )
        message.save()
        messages = Message.objects.filter(chat=chat)
        print(messages)
        return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages})

@login_required
def create_chat(request, username):
    current_user = request.user
    other_user = get_object_or_404(User, login=username)

    if current_user.id > other_user.id:
        room_name = f'{current_user.id}_{other_user.id}'
    else:
        room_name = f'{other_user.id}_{current_user.id}'
    return redirect('get_chat', room_name)

@login_required
def chat_view(request):
    if request.method == "GET":
        chats = Chat.objects.filter(sender=request.user).order_by('-id')
        return render(request, 'chat/chat_list.html', {'chats': chats})
