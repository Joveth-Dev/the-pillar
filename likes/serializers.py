from rest_framework import serializers
from .models import LikedItem, DislikedItem


class LikedItemSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_id = self.context['user_id']
        return LikedItem.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = LikedItem
        fields = ['id', 'content_type', 'object_id', 'user_id']


class DislikedItemSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_id = self.context['user_id']
        return DislikedItem.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = DislikedItem
        fields = ['id', 'content_type', 'object_id', 'user_id']
