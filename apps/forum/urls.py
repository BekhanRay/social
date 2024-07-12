from django.urls import path

from apps.forum import views

urlpatterns = [
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/thread/<int:thread_id>/', views.post_list, name='post_list'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/dislike/', views.dislike_comment, name='dislike_comment'),
    path('thread/<int:thread_id>/add_post/', views.add_post, name='add_post'),
]