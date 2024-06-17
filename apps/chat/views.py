from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def create_or_get_chat(request, recipient_id):
    sender = request.user
    recipient = get_object_or_404(User, id=recipient_id)

    # Проверяем, существует ли уже чат между этими пользователями
    chat = Chat.objects.filter(sender=sender, receiver=recipient).first()
    if not chat:
        # Если чата нет, создаем новый чат
        chat = Chat.objects.create(sender=sender, receiver=recipient)

    return redirect('chat_detail', chat_id=chat.id)

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all()

    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        chat_id = request.POST.get('chat_id')
        content = request.POST.get('content')

        chat = get_object_or_404(Chat, id=chat_id)
        if sender == chat.sender or sender == chat.receiver:
            message = Message.objects.create(chat=chat, sender=sender, content=content)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Вы не можете отправлять сообщения в этот чат.'})

    return JsonResponse({'success': False, 'error': 'Метод не поддерживается.'})
