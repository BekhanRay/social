from .consumers import ChatConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'chat/(?P<id>\w+)/$', ChatConsumer.as_asgi()),
]