from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from . models import Profile
from . serializers import ProfilesSerializer


class ProfileViewSet(CreateModelMixin,
                     GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilesSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    @method_decorator(cache_page(10*60, key_prefix='profiles_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        profile = Profile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ProfilesSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ProfilesSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
