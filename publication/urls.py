from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('members', views.MemberViewSet)
router.register('issues', views.IssueViewSet, basename='issues')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('announcements', views.AnnouncementViewSet)

urlpatterns = router.urls
