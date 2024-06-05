from django.contrib import admin

from .models import Forum, Thread

# Register your models here.
admin.site.register(Forum)
admin.site.register(Thread)