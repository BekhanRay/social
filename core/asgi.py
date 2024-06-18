# """
# ASGI config for core project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """
#
# import os
#
# # from channels import routing
# from apps.chat.routing import websocket_urlpatterns
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
#
# asgi_application = get_asgi_application()
#
# application = ProtocolTypeRouter(
#     {"http": asgi_application,
#      "websocket": AllowedHostsOriginValidator(
#          AuthMiddlewareStack(
#             URLRouter(websocket_urlpatterns)
#      ))
#      }
# )

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chat import routing
import socketio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

# Создаем сервер Socket.IO
sio = socketio.Server()

# Создаем приложение ASGI
django_asgi_app = get_asgi_application()

# Объединяем Django и Socket.IO в одном приложении
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
    "socketio": socketio.ASGIApp(sio),
})
