from rest_framework import serializers
from . models import Profile


class ProfilesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    def get_first_name(self, profile):
        return profile.user.first_name

    def get_last_name(self, profile):
        return profile.user.last_name

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Profile.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'first_name', 'last_name', 'profile_image', 'birth_date',
                  'sex', 'city', 'state_or_province', 'zip_code', 'country']
