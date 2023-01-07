from djoser.serializers import UserSerializer as BaseUserSerializer, \
    UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email',
                  'last_name', 'first_name', 'middle_initial']


class UserSerializer(BaseUserSerializer):
    sex = serializers.SerializerMethodField(read_only=True)

    def get_sex(self, user):
        return user.profile.sex

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'avatar', 'username', 'email',
                  'last_name', 'first_name', 'middle_initial', 'sex']
