
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Forum, Thread, Post, Comment, CommentReaction


def forum_list(request):
    forums = Forum.objects.prefetch_related('threads').all()
    return render(request, 'forum_list.html', {'forums': forums})


def post_list(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    posts = Post.objects.filter(thread=thread_id)
    return render(request, 'post_list.html', {'posts': posts,
                                              'thread': thread})


def post_detail(request, thread_id, post_id):
    thread = Thread.objects.get(id=thread_id)
    post = Post.objects.get(id=post_id)
    return render(request, 'post_detail.html', {'post': post,
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
            if 'photo' in request.FILES.keys():
                post.photo = request.FILES['photo']
            post.save()
            return redirect(reverse('post_list', args=[thread_id]))
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
            return redirect('post_list', thread_id=post.thread.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('post_list', thread_id=comment.post.thread.id)


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
    return redirect('post_list', thread_id=comment.post.thread.id)


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
    return redirect('post_list', thread_id=comment.post.thread.id)

