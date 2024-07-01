from django.contrib import admin

from .models import Forum, Thread, Post, Comment

# Register your models here.
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Comment)
