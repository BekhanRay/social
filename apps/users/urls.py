from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import register, login_view, profile, logout_view, profile_detail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', login_required(profile), name='profile'),
    path('logout/', logout_view, name='logout'),
    path('profile_detail/', profile_detail, name='profile_detail')
]
