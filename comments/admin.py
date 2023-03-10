from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'commenter', 'message', 'comment_date',
                    'commented_item_type', 'content_id', 'content_name']

    @admin.display(ordering='user')
    def commenter(self, comment):
        return comment.user.get_full_name()

    @admin.display(ordering='content_type', description='Content type')
    def commented_item_type(self, comment):
        return comment.content_type.model

    @admin.display(ordering='object_id', description='Content ID')
    def content_id(self, comment):
        return comment.object_id

    @admin.display(ordering='content_type', description='Content name')
    def content_name(self, comment):
        try:
            if comment.content_type.model == 'article':
                return comment.content_object
            return f'Volume {comment.content_object.volume_number} | Issue {comment.content_object}'
        except AttributeError:
            return comment.content_object


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment_number',
                    'commenter', 'message', 'reply_date']
    list_select_related = ['comment']

    @admin.display(ordering='comment', description='Comment ID')
    def comment_number(self, reply):
        return reply.comment

    @admin.display(ordering='user')
    def commenter(self, reply):
        return reply.user.get_full_name()
