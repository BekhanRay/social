import socketio
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()
sio = socketio.AsyncServer(async_mode='asgi')

@sio.event
async def connect(sid, environ):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def join_chat(sid, data):
    chat_id = data['chat_id']
    await sio.enter_room(sid, chat_id)
    print(f"Socket {sid} joined room {chat_id}")

@sio.event
async def leave_chat(sid, data):
    chat_id = data['chat_id']
    await sio.leave_room(sid, chat_id)
    print(f"Socket {sid} left room {chat_id}")

@sio.event
async def send_message(sid, data):
    chat_id = data['chat_id']
    sender_id = data['sender_id']
    message = data['message']

    sender = await sync_to_async(User.objects.get)(id=sender_id)
    chat = await sync_to_async(Chat.objects.get)(id=chat_id)
    await sync_to_async(Message.objects.create)(chat=chat, sender=sender, content=message)

    await sio.emit('receive_message', {'message': message, 'sender': sender.username}, room=chat_id)
