from django.contrib import admin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


@admin.register(models.College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'courses_offered']
    search_fields = ['title__icontains', 'degreeprograms__title__istartswith']
    ordering = ['title']

    @admin.display(ordering='courses_offered')
    def courses_offered(self, college):
        url = (
            reverse('admin:university_degreeprogram_changelist')
            + '?'
            + urlencode({
                'college__id': str(college.id)
            }))
        return format_html('<a href={}>{}</a>', url, college.courses_offered)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(courses_offered=Count('degreeprograms'))


@admin.register(models.DegreeProgram)
class DegreeProgramAdmin(admin.ModelAdmin):
    autocomplete_fields = ['college']
    list_display = ['id', 'title', 'college']
    list_filter = ['college']
    list_per_page = 10
    list_select_related = ['college']
    ordering = ['college']
    search_fields = ['title__icontains']


@ admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    fields = ['display_picture', 'profile',
              'student_id', 'college', 'degree_program']
    autocomplete_fields = ['profile', 'college', 'degree_program']
    list_display = ['picture', 'student_id',
                    'full_name', 'college', 'degree_program']
    list_filter = ['student_id', 'college', 'degree_program']
    list_per_page = 10
    list_select_related = ['profile__user', 'degree_program', 'college']
    ordering = ['student_id']
    readonly_fields = ['display_picture']
    search_fields = ['student_id__iexact', 'profile__user__first_name__istartswith',
                     'profile__user__first_name__istartswith', 'college__title__icontains', 'degree_program__title__icontains']

    def display_picture(self, instance):
        if instance.profile.profile_image.name != '':
            return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile"/>')
        else:
            if instance.profile.sex == 'M':
                instance.profile.profile_image = 'userprofile/images/default_male.jpg'
                return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile"/>')
            elif instance.user.profile.sex == 'F':
                instance.profile.profile_image = 'userprofile/images/default_female.jpg'
                return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile"/>')

    @admin.display(ordering='profile__user__first_name')
    def name(self, student):
        return student.profile.user.get_full_name()

    @admin.display(ordering='id')
    def picture(self, instance):
        if instance.profile.profile_image.name != '':
            return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile_icon"/>')
        else:
            if instance.profile.sex == 'M':
                instance.profile.profile_image = 'userprofile/images/default_male.jpg'
                return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile_icon"/>')
            elif instance.profile.sex == 'F':
                instance.profile.profile_image = 'userprofile/images/default_female.jpg'
                return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile_icon"/>')

    @ admin.display(ordering='user__first_name')
    def full_name(self, student: models.Student):
        return student.profile.user.get_full_name()

    class Media:
        css = {
            'all': ['university/styles.css']
        }


@admin.register(models.StudentPulse)
class StudentPulseAdmin(admin.ModelAdmin):
    fields = ['description']
    list_display = ['id', 'description', 'date_created']
    list_filter = ['date_created']
    readonly_fields = ['student']
    search_fields = ['id__exact', 'description__icontains']

    def save_model(self, request, obj, form, change):
        obj.student = request.user.profile.student
        return super().save_model(request, obj, form, change)
