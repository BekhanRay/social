# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# from .models import Chat, Message
# from ..users.models import CustomUser
#
# User = get_user_model()
#
# @login_required
# def get_chat(request, room_name):
#     print('get_chat')
#     if request.method == "GET":
#         chat = Chat.objects.get(room_name=room_name)
#         messages = Message.objects.filter(chat=chat).order_by('-timestamp')
#         receiver = CustomUser.objects.get(id=chat.receiver.id)
#         print(messages)
#         return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages, 'receivers': receiver})
#
#     elif request.method == "POST":
#         sender = request.user
#         if str(room_name).split('_')[0] != sender.id:
#             receiver = str(room_name).split('_')[0]
#         else:
#             receiver = str(room_name).split('_')[1]
#         receiver = User.objects.get(id=receiver)
#         print(receiver, sender)
#         chat = Chat.objects.get(room_name=room_name)
#         message = Message.objects.create(
#             chat=chat,
#             sender=receiver,
#             message=request.POST['message'],
#         )
#         message.save()
#         messages = Message.objects.filter(chat=chat)
#         print(messages)
#         return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages})
#
# @login_required
# def create_chat(request, username):
#     current_user = request.user
#     other_user = User.objects.get(login=username)
#
#     if current_user.id > other_user.id:
#         room_name = f'{current_user.id}_{other_user.id}'
#     else:
#         room_name = f'{other_user.id}_{current_user.id}'
#
#     Chat.objects.create(
#         room_name=room_name,
#         sender=current_user,
#         receiver=other_user,
#     )
#
#     return redirect('get_chat', room_name)
#
# # @login_required
# # def chat_view(request):
# #     if request.method == "GET":
# #         chats = Chat.objects.filter(sender=request.user).prefetch_related('Messages', 'CustomUser')
# #         users = CustomUser.objects.filter()
# #         return render(request, 'chat/chat_list.html', {'chats': chats, 'users': request.user })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Chat, Message
from ..users.models import CustomUser

User = get_user_model()

@login_required
def get_chat(request, room_name):
    chat = get_object_or_404(Chat, room_name=room_name)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    receiver = CustomUser.objects.get(id=chat.receiver.id)
    current_user = CustomUser.objects.get(id=chat.sender.id)
    chats = Chat.objects.filter(sender=current_user).union(Chat.objects.filter(receiver=current_user))
    print(receiver.avatar_photo.file_path.url)
    return render(request, 'chat/chat.html', {
        'chat': chat,
        'chats': chats,
        'messages': messages,
        'receiver': receiver,
        'current_user_avatar': current_user.avatar_photo.file_path.url if current_user.avatar_photo else 'user_photos/default_user_photo.jpg',
        'other_user_avatar': current_user.avatar_photo.file_path.url if receiver.avatar_photo else 'user_photos/default_user_photo.jpg',
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
