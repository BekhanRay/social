from .consumers import ChatConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<id>\w+)/$', ChatConsumer.as_asgi()),
]