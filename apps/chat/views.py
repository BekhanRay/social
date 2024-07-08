from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404

from .models import Chat, Message

User = get_user_model()


@login_required
def get_chat(request, room_name):
    chat = get_object_or_404(Chat, room_name=room_name)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    current_user = request.user
    receiver = chat.receiver
    latest_message_subquery = Message.objects.filter(
        chat=OuterRef('pk')
    ).order_by('-timestamp').values('timestamp')[:1]

    # Filter chats for the current user and annotate with the latest message time
    chats = Chat.objects.filter(
        Q(sender=current_user) | Q(receiver=current_user)
    ).annotate(
        last_message_time=Coalesce(Subquery(latest_message_subquery), None)
    ).order_by('-last_message_time')
    return render(request, 'chat/chat.html', {
        'chat': chat,
        'chats': chats,
        'messages': messages,
        'receiver': receiver,
        'current_user_avatar': current_user.avatar_photo.file_path.url if current_user.avatar_photo else 'user_photos/default_user_photo.jpg',
        'other_user_avatar': receiver.avatar_photo.file_path.url if receiver.avatar_photo else 'user_photos/default_user_photo.jpg',
    })


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

    return redirect('get_chat', room_name)

@login_required
def chat_list_view(request):
    current_user = request.user
    chats = Chat.objects.filter(sender=current_user).union(Chat.objects.filter(receiver=current_user))
    return render(request, 'chat/chat_list.html', {'chats': chats, 'current_user': current_user})
