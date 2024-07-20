from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser, Photo, Profile, Favorite, Promotion, UserPromotion

admin.site.register(CustomUser)
admin.site.register(Favorite)
admin.site.register(Photo)
admin.site.register(Profile)
admin.site.unregister(Group)
admin.site.site_header = 'Админка'
 
 
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserPromotion)
class UserPromotionAdmin(admin.ModelAdmin):
    list_display = ['user', 'promotion', 'is_participating']
    list_filter = ['is_participating']
    search_fields = ['user__username', 'promotion__title']
