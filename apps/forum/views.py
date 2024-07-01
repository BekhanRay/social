
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm, PostForm
from .models import Forum, Thread, Post, Comment, CommentReaction


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
                                              'thread': thread})


@login_required
def add_post(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect('')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form, 'thread': thread})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_list', forum_id=post.thread.forum.id, thread_id=post.thread.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


@login_required
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = parent_comment.post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            return redirect('post_list', forum_id=parent_comment.post.thread.forum.id, thread_id=parent_comment.post.thread.id)
    else:
        form = CommentForm()
    return render(request, 'reply_comment.html', {'form': form, 'parent_comment': parent_comment})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('post_list', forum_id=comment.post.thread.forum.id, thread_id=comment.post.thread.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_list', forum_id=comment.post.thread.forum.id, thread_id=comment.post.thread.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('post_list', forum_id=comment.post.thread.forum.id, thread_id=comment.post.thread.id)


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    reaction, created = CommentReaction.objects.get_or_create(user=request.user, comment=comment)
    if reaction.reaction_type != 'like':
        comment.likes += 1
        if reaction.reaction_type == 'dislike':
            comment.dislikes -= 1
        reaction.reaction_type = 'like'
        reaction.save()
        comment.save()
    return redirect('post_list', forum_id=comment.post.thread.forum.id, thread_id=comment.post.thread.id)


@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    reaction, created = CommentReaction.objects.get_or_create(user=request.user, comment=comment)
    if reaction.reaction_type != 'dislike':
        comment.dislikes += 1
        if reaction.reaction_type == 'like':
            comment.likes -= 1
        reaction.reaction_type = 'dislike'
        reaction.save()
        comment.save()
    return redirect('post_list', forum_id=comment.post.thread.forum.id, thread_id=comment.post.thread.id)

