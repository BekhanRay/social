# from django.urls import path
# from .consumers import *
#
# websocket_urlpatterns = [
#     path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()),
#     path("ws/online-status/", OnlineStatusConsumer.as_asgi()),
# ]
from consumers import ChatConsumer
from django.urls import re_path, path


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    # path('ws/<int:id>/', PersonalChatConsumer.as_asgi())

]