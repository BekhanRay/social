from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:recipient_id>/', views.create_or_get_chat, name='create_or_get_chat'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('send-message/', views.send_message, name='send_message'),
]
