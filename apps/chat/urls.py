from django.urls import path
from . import views

urlpatterns = [
    path('<str:room_name>/', views.get_chat, name='get_chat'),
    path('create/<str:username>/', views.create_chat, name='create_chat'),
    path('', views.chat_view, name='chat_view'),
]
