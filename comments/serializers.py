from rest_framework import serializers
from . models import Comment, Reply


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Comment.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'message', 'comment_date',
                  'content_type', 'object_id']


class ReplySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Reply.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = Reply
        fields = ['id', 'user_id', 'comment', 'message', 'reply_date']
