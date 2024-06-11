from django.urls import path, re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r"ws/chat/<uuid>", ChatConsumer.as_asgi()),
    # path('ws/user/<token>', UserConsumer.as_asgi()),
]