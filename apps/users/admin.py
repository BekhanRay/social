from django.contrib import admin
<<<<<<< HEAD
from django.contrib.auth.models import Group

from .models import CustomUser, UserAction, Photo, Profile, Video, Action, Search, Statistics, Forum, Favorite

admin.site.register(CustomUser)
admin.site.register(UserAction)
admin.site.register(Favorite)
admin.site.register(Photo)
admin.site.register(Profile)
admin.site.register(Video)
admin.site.register(Action)
admin.site.register(Search)
admin.site.register(Statistics)
admin.site.register(Forum)
admin.site.unregister(Group)
admin.site.site_header = 'Админка'
=======

# Register your models here.
>>>>>>> 7315cff (Initial commit)
