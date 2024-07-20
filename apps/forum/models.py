
from apps.users.models import CustomUser
from django.db import models


class Forum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Thread(models.Model):
    forum = models.ForeignKey(Forum, related_name='threads', on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    content = models.TextField()
    title = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def count_comments(self):
        return self.comments.count()

    def __str__(self):
        return f"Опубликовано {self.author} в {self.thread}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Commented by {self.author} to {self.post} post'

    @property
    def get_dislikes(self):
        count = self.dislikes
        if not count:
            return ''
        return count

    @property
    def get_likes(self):
        count = self.likes
        if not count:
            return ''
        return count


class CommentReaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10)  # 'like' or 'dislike'

    class Meta:
        unique_together = ('user', 'comment')

