from django.contrib import admin
from .models import User, UserAction, Photo, Profile, Video, Action, Search, Statistics, Message, Forum

admin.site.register(User)
admin.site.register(UserAction)
admin.site.register(Photo)
admin.site.register(Profile)
admin.site.register(Video)
admin.site.register(Action)
admin.site.register(Search)
admin.site.register(Statistics)
admin.site.register(Message)
admin.site.register(Forum)