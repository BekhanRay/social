from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('code_confirmation/', views.register, name='code_confirmation'),
    # акции
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/<int:promotion_id>/print/', views.print_flyer, name='print_flyer'),

    path('add_favorite/<int:user_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:user_id>/', views.remove_favorite, name='remove_favorite'),
    path('login/', views.login_view, name='login'),
    path('logout/', login_required(views.logout_view), name='logout'),
    path('profile/', login_required(views.profile), name='profile'),
    path('delete_gallery_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('user/<int:user_id>/', login_required(views.user_detail), name='user_detail'),
    path('profile/change/', views.user_change, name='user_change'),
    path('user_agreement/', views.user_agreement, name='user_agreement'),
    path('password-change/', views.UserPasswordChange.as_view(), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="password_change_done.html"), name="password_change_done"),
    path('password-reset/',
         views.CustomPasswordResetView.as_view(
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