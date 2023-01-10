from django.db.models.aggregates import Count
from django.db.models import OuterRef, Subquery
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from .pagination import DefaultPagination
from .models import Announcement, Article, Issue, Member, MemberPosition, Banner
from .serializers import AnnouncementSerializer, \
    ArticleSerializer, \
    BannerSerializer, \
    IssueSerializer, \
    MemberSerializer


class MemberViewSet(ReadOnlyModelViewSet):
    # get the current position of the members first
    subquery = MemberPosition.objects.select_related('position').filter(
        member_id=OuterRef('pk')).order_by('-date_assigned').values('position__title')[:1]

    # annotate the queryset with their current position
    queryset = Member.objects.prefetch_related('memberposition_set').select_related(
        'user__profile').annotate(current_position=Subquery(subquery)).filter(user__is_active=True).defer('date_updated')
    serializer_class = MemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__last_name',
                     'user__middle_initial', 'pen_name']

    @method_decorator(cache_page(10*60, key_prefix='members_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class IssueViewSet(ReadOnlyModelViewSet):
    queryset = Issue.objects.select_related('issuefile') \
        .annotate(articles_count=Count('articles')) \
        .defer('date_created', 'is_approved', 'is_enabled') \
        .filter(is_approved=True) \
        .filter(is_enabled=True)
    serializer_class = IssueSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'id']
    ordering_fields = ['date_published',
                       'date_updated', 'volume_number', 'issue_number']
    pagination_class = DefaultPagination
    search_fields = ['volume_number', 'issue_number', 'description']

    @method_decorator(cache_page(10*60, key_prefix='issues_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.select_related('member__user') \
        .defer('member__date_updated') \
        .defer('member__user__password',
               'member__user__last_login',
               'member__user__is_superuser',
               'member__user__username',
               'member__user__is_staff',
               'member__user__is_active',
               'member__user__date_joined',
               'member__user__email') \
        .prefetch_related('article_images') \
        .defer('slug', 'date_created', 'is_approved', 'is_enabled') \
        .filter(is_approved=True) \
        .filter(is_enabled=True)
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,
                       OrderingFilter]
    filterset_fields = ['category', 'id']
    ordering_fields = ['date_published', 'date_published']
    pagination_class = DefaultPagination
    search_fields = ['title_or_headline', 'body', 'member__pen_name',
                     'member__user__first_name', 'member__user__last_name']

    @method_decorator(cache_page(10*60, key_prefix='articles_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AnnouncementViewSet(ReadOnlyModelViewSet):
    queryset = Announcement.objects.filter(is_approved=True)
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_created']
    serializer_class = AnnouncementSerializer

    @method_decorator(cache_page(10*60, key_prefix='announcements_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BannerViewSet(ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_approved=True)
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_created']
    serializer_class = BannerSerializer

    @method_decorator(cache_page(10*60, key_prefix='banners_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
