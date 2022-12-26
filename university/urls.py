from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('students', views.StudentViewSet)
router.register('colleges', views.CollegeViewSet)
router.register('degree_programs', views.DegreeProgramViewSet)

students_router = routers.NestedDefaultRouter(
    router, 'students', lookup='student')
students_router.register(
    'studentpulses', views.StudentPulseViewSet, basename='student-studentpulse')

urlpatterns = router.urls + students_router.urls
