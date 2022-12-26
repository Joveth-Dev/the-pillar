from rest_framework import serializers
from . models import Profile


class ProfilesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Profile.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'profile_image', 'birth_date',
                  'sex', 'city', 'state_or_province', 'zip_code', 'country', 'is_student']
