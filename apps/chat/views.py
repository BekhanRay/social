from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Chat, Message
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    return render(request, "chat/index.html")

# @login_required
# def get_or_create_chat(request, room):
#     if request.method == "GET":
#         # print(request.user)
#         if request.user.is_authenticated:
#             if Chat.objects.filter(room_name=room).exists():
#                 return render(request, "chat/chat.html", {'messages': Message.objects.filter(chat=room)})
#
#             new_room = Chat.objects.create(
#                 room_name=room,
#                 sender=request.user,
#                 receiver=User.objects.get(username=room).id,
#             )
#             new_room.save()
#     return render(request, "chat/chat.html", {'messages': Message.objects.filter(chat=room)})

# @login_required
# def get_or_create_chat(request, room):
#     if request.method == "GET":
#         try:
#             chat = Chat.objects.get(room_name=room)
#         except Chat.DoesNotExist:
#             receiver_user = get_object_or_404(User, username=room)
#             chat = Chat.objects.create(
#                 room_name=room,
#                 sender=request.user,
#                 receiver=receiver_user
#             )
#             chat.save()
#             return redirect('chat:get_or_create_chat', room=room)  # Redirect to avoid resubmission on refresh
#
#         messages = Message.objects.filter(chat=chat)
#         return render(request, "chat/chat.html", {'messages': messages})
#     return HttpResponse(status=405)  # Method not allowed for non-GET requests

@login_required
def get_or_create_chat(request, room):
    if request.method == "GET":
        chat, created = Chat.objects.get_or_create(
            room_name=room,
            defaults={'sender': request.user, 'receiver': User.objects.get(login=room)}
        )

        messages = Message.objects.filter(chat=chat)
        return render(request, "chat/chat.html", {'room_name': room, 'messages': messages})

    elif request.method == "POST":
        message = Message.objects.create(
            chat=room,
            sender=request.user,
            message=request.POST['message'],
        )
        message.save()
        messages = Message.objects.filter(chat=room)
        return render(request, "chat/chat.html", {'room_name': room, 'messages': messages})
    return HttpResponse(status=405)  # Method not allowed for non-GET requests