from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination
from .models import LikedItem, DislikedItem
from .serializers import LikedItemSerializer, DislikedItemSerializer


class LikedItemViewSet(ModelViewSet):
    queryset = LikedItem.objects.select_related('content_type'). \
        select_related('user'). \
        filter(Q(content_type=8) | Q(content_type=9))
    serializer_class = LikedItemSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['content_type', 'object_id']

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class DislikedItemViewSet(ModelViewSet):
    queryset = DislikedItem.objects.select_related('content_type'). \
        select_related('user'). \
        filter(Q(content_type=8) | Q(content_type=9))
    serializer_class = DislikedItemSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['content_type', 'object_id']

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
