from django.contrib import admin
from django.utils.html import format_html
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ['display_picture', 'profile_image', 'user', 'birth_date',
              'sex', 'city', 'state_or_province', 'zip_code', 'country']
    list_display = ['profile', 'first_name', 'last_name', 'birth_date', 'sex',
                    'city', 'state_or_province', 'zip_code', 'country']
    list_filter = ['sex', 'city',
                   'state_or_province', 'zip_code', 'country']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    readonly_fields = ['display_picture']
    search_fields = ['user__first_name', 'user__last_name', 'city__istartswith', 'state_or_province__istartswith',
                     'country__istartswith']

    def display_picture(self, instance):
        if instance.profile_image.name != '':
            return format_html(f'<img src="{instance.profile_image.url}" class="profile"/>')
        else:
            if instance.sex == 'M':
                instance.profile_image.name = 'userprofile/images/default_male.jpg'
                return format_html(f'<img src="{instance.profile_image.url}" class="profile"/>')
            elif instance.sex == 'F':
                instance.profile_image.name = 'userprofile/images/default_female.jpg'
                return format_html(f'<img src="{instance.profile_image.url}" class="profile"/>')
        # return format_html(f'<img src="{instance.profile_image.url}" class="profile"/>')

    @admin.display(ordering='id')
    def profile(self, instance):
        if instance.profile_image.name != '':
            return format_html(f'<img src="{instance.profile_image.url}" class="profile_icon"/>')
        else:
            if instance.sex == 'M':
                instance.profile_image = 'userprofile/images/default_male.jpg'
                return format_html(f'<img src="{instance.profile_image.url}" class="profile_icon"/>')
            elif instance.sex == 'F':
                instance.profile_image = 'userprofile/images/default_female.jpg'
                return format_html(f'<img src="{instance.profile_image.url}" class="profile_icon"/>')
        # return format_html(f'<img src="{instance.profile_image.url}" class="profile_icon"/>')

    class Media:
        css = {
            'all': ['userprofile/styles.css']
        }
