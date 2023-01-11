from django.contrib import admin
from .models import LikedItem, DislikedItem

# Register your models here.


@admin.register(LikedItem)
class LikedItemAdmin(admin.ModelAdmin):
    fields = ['content_type', 'object_id']
    list_display = ['id', 'liked_item_id',
                    'liked_item_type', 'liked_item_name', 'liked_by']
    list_select_related = ['content_type', 'user']
    search_fields = ['object_id',
                     'content_type__model', 'user__username']

    @admin.display(ordering='object_id')
    def liked_item_id(self, likeditem):
        return likeditem.object_id

    @admin.display(ordering='content_type')
    def liked_item_type(self, likeditem):
        return likeditem.content_type.model

    @admin.display(ordering='content_object')
    def liked_item_name(self, likeditem):
        if likeditem.content_type.model == 'article':
            return likeditem.content_object
        return f'Volume {likeditem.content_object.volume_number} | Issue {likeditem.content_object}'

    @admin.display(ordering='user__username')
    def liked_by(self, likeditem):
        return likeditem.user

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(DislikedItem)
class DislikedItemAdmin(admin.ModelAdmin):
    fields = ['content_type', 'object_id']
    list_display = ['id', 'disliked_item_id',
                    'disliked_item_type', 'disliked_item_name', 'disliked_by']
    list_select_related = ['content_type', 'user']
    search_fields = ['object_id',
                     'content_type__model', 'user__username']

    @admin.display(ordering='object_id')
    def disliked_item_id(self, likeditem):
        return likeditem.object_id

    @admin.display(ordering='content_type')
    def disliked_item_type(self, likeditem):
        return likeditem.content_type.model

    @admin.display(ordering='content_object')
    def disliked_item_name(self, likeditem):
        if likeditem.content_type.model == 'article':
            return likeditem.content_object
        return f'Volume {likeditem.content_object.volume_number} | Issue {likeditem.content_object}'

    @admin.display(ordering='user__username')
    def disliked_by(self, likeditem):
        return likeditem.user

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)
