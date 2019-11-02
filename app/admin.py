from django.contrib import admin
from .models import Photo, Category, Like, Follow

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'photos')
    list_display_links = ('id', 'user', 'photos')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')
    list_display_links = ('id', 'follower', 'following')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)