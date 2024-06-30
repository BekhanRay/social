# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('<str:room_name>/', views.get_chat, name='get_chat'),
#     path('create/<str:username>/', views.create_chat, name='create_chat'),
#     # path('', views.chat_view, name='chat_view'),
# ]
from django.urls import path
from .views import get_chat, create_chat, chat_list_view
from ..users.views import chat_bridge

urlpatterns = [
    path('<str:room_name>/', get_chat, name='get_chat'),
    path('create/<str:username>/', create_chat, name='create_chat'),
    path('chat_bridge/<str:username>/', chat_bridge, name='chat_bridge'),
    path('', chat_list_view, name='chat_list'),
]
