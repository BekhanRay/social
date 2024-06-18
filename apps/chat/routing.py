# from django.urls import path
# from .consumers import ChatConsumer
#
# websocket_urlpatterns = [
#     path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
# ]
from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
]
