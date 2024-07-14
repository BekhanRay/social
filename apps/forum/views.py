from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import PostForm
from .models import Forum, Thread, Post, Comment, CommentReaction


def forum_list(request):
    forums = Forum.objects.prefetch_related('threads').all()
    return render(request, 'forum_list.html', {'forums': forums})


def post_list(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    posts = Post.objects.filter(thread=thread_id)
    return render(request, 'pages/posts_list.html', {'posts': posts,
                                                     'thread': thread})


def post_detail(request, thread_id, post_id):
    thread = Thread.objects.get(id=thread_id)
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=request.POST.get('comment', None)
        )
        comment.save()
    return render(request, 'pages/post_detail.html', {'post': post,
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
    return redirect('post_detail', thread_id=comment.post.thread.id, post_id=comment.post.id)


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
    return redirect('post_detail', thread_id=comment.post.thread.id, post_id=comment.post.id)

