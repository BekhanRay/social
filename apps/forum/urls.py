from django.urls import path

from .views import forum_list, thread_list, post_list

urlpatterns = [
    path('forums/', forum_list, name='forum_list'),
    path('forums/<int:forum_id>/threads/', thread_list, name='thread_list'),
    path('forums/<int:forum_id>/threads/<int:thread_id>/posts/', post_list, name='post_list')

]