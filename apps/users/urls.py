from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import register, login_view, profile, user_detail
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', login_required(profile), name='profile'),
    path('user/<int:user_id>/', user_detail, name='user_detail'),

    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]