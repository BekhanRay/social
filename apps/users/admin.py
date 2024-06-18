from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, UserAction, Profile, Video, Action, Search, Statistics, Forum


admin.site.unregister(Group)

admin.site.register(CustomUser)
admin.site.register(UserAction)
admin.site.register(Profile)
admin.site.register(Video)
admin.site.register(Action)
admin.site.register(Search)
admin.site.register(Statistics)
admin.site.register(Forum)
admin.site.site_header = 'Amici admin'
