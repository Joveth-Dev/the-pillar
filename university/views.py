from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from .pagination import DefaultPagination
from .models import College, DegreeProgram, Student, StudentPulse
from .serializers import CollegeSerializer, DegreeProgramSerializer, StudentPulseSerializer, StudentSerializer


class CollegeViewSet(ReadOnlyModelViewSet):
    queryset = College.objects.annotate(
        courses_offered=Count('degreeprograms'))
    serializer_class = CollegeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']


class DegreeProgramViewSet(ReadOnlyModelViewSet):
    queryset = DegreeProgram.objects.select_related('college').all()
    pagination_class = DefaultPagination
    serializer_class = DegreeProgramSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']


class StudentViewSet(CreateModelMixin,
                     GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        student = Student.objects.get(
            profile_id=request.user.profile.id)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class StudentPulseViewSet(ListModelMixin,
                          CreateModelMixin,
                          RetrieveModelMixin,
                          GenericViewSet):
    serializer_class = StudentPulseSerializer

    def get_queryset(self):
        return StudentPulse.objects.filter(student_id=self.kwargs['student_pk'])

    def get_serializer_context(self):
        return {'student_id': self.kwargs['student_pk']}
