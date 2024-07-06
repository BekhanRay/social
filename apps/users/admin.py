from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser, Photo, Profile, Video, Forum, Favorite

admin.site.register(CustomUser)
admin.site.register(Favorite)
admin.site.register(Photo)
admin.site.register(Profile)
admin.site.register(Video)
admin.site.register(Forum)
admin.site.unregister(Group)
admin.site.site_header = 'Админка'


