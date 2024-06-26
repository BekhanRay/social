from django.urls import path
from . import views

urlpatterns = [
    path('messages/<str:username>/', views.ChatMessageList.as_view(), name='message-list'),
    path('messages/create/', views.ChatMessageCreate.as_view(), name='message-create'),
    path('chat/<str:username>/', views.chat_view, name='chat-view'),
]
