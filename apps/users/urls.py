from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, login_view, profile, user_detail, logout_view, user_change, favorite_list, add_favorite, \
    remove_favorite

# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('favorites/', favorite_list, name='favorites'),
    path('add_favorite/<int:user_id>/', add_favorite, name='add_favorite'),
    path('remove_favorite/<int:user_id>/', remove_favorite, name='remove_favorite'),
    path('login/', login_view, name='login'),
    path('profile/', login_required(profile), name='profile'),
    path('user/<int:user_id>/', user_detail, name='user_detail'),
    path('profile/change/', user_change, name='user_change'),

    path('logout/', logout_view, name='logout'),
]