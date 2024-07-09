from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from .views import register, login_view, profile, user_detail, logout_view, user_change, favorite_list, add_favorite, \
    remove_favorite, user_agreement, UserPasswordChange, CustomPasswordResetView, index_page

urlpatterns = [
    path('register/', register, name='register'),
    path('favorites/', favorite_list, name='favorites'),
    path('add_favorite/<int:user_id>/', add_favorite, name='add_favorite'),
    path('remove_favorite/<int:user_id>/', remove_favorite, name='remove_favorite'),
    path('login/', login_view, name='login'),
    path('profile/', login_required(profile), name='profile'),
    path('user/<int:user_id>/', user_detail, name='user_detail'),
    path('profile/change/', user_change, name='user_change'),
    path('user_agreement/', user_agreement, name='user_agreement'),
    path('logout/', logout_view, name='logout'),


    path('password-change/', UserPasswordChange.as_view(), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="password_change_done.html"), name="password_change_done"),
    path('password-reset/',
         CustomPasswordResetView.as_view(
            template_name="password_reset_form.html",
            email_template_name="password_reset_email.html",
            success_url=reverse_lazy("password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name='password_reset_complete'),
]