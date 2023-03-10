from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.CommentViewSet)

comments_router = routers.NestedDefaultRouter(
    router, '', lookup='comment')
comments_router.register(
    'replies', views.ReplyViewSet, basename='comment-reply')

urlpatterns = router.urls + comments_router.urls
