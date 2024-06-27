
from .views import index, get_or_create_chat
from django.urls import path


urlpatterns = [
    path('<room>/', get_or_create_chat, name="chat_view")
]
