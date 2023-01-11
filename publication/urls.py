from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('members', views.MemberViewSet)
router.register('issues', views.IssueViewSet, basename='issues')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('announcements', views.AnnouncementViewSet)
router.register('banners', views.BannerViewSet)

urlpatterns = router.urls
