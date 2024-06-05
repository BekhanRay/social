from django.shortcuts import render
from .models import Forum, Thread, Post


def forum_list(request):
    forums = Forum.objects.all()
    return render(request, 'forum_list.html', {'forums': forums})


def thread_list(request, forum_id):
    threads = Thread.objects.filter(forum=forum_id)
    forum = Forum.objects.get(id=forum_id)
    return render(request, 'thread_list.html', {'threads': threads,
                                                'forum_title': forum.title})


def post_list(request, forum_id, thread_id):
    thread = Thread.objects.get(id=thread_id)
    posts = Post.objects.filter(thread=thread_id)
    return render(request, 'post_list.html', {'posts': posts,
                                              'thread_title': thread.title})


