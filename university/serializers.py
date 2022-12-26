from pprint import pprint
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import College, DegreeProgram, Student, StudentPulse


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'title', 'courses_offered']

    courses_offered = serializers.IntegerField(read_only=True)


class DegreeProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = DegreeProgram
        fields = ['id', 'title', 'college_name']

    college_name = serializers.SerializerMethodField(
        method_name='get_college_name')

    def get_college_name(self, degree_program: DegreeProgram):
        return degree_program.college.title


class StudentSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(read_only=True)
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, student):
        return student.profile.user.get_full_name()

    class Meta:
        model = Student
        fields = ['id', 'profile_id', 'student_id',
                  'full_name', 'college', 'degree_program']


class StudentPulseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPulse
        fields = ['id', 'description', 'date_created']

    def create(self, validated_data):
        student_id = self.context['student_id']
        return StudentPulse.objects.create(student_id=student_id, **validated_data)
