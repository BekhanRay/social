from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import register, user_login, profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('profile/', login_required(profile), name='profile')
]
