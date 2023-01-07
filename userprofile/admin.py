from django.contrib import admin
from django.utils.html import format_html
from . import models
from . cache_handler import delete_cache_with_key_prefix


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ['avatar_diplay', 'user', 'birth_date', 'sex',
              'city', 'state_or_province', 'zip_code', 'country']
    list_display = ['user_avatar', 'first_name', 'last_name', 'birth_date', 'sex',
                    'city', 'state_or_province', 'zip_code', 'country']
    list_filter = ['sex', 'city',
                   'state_or_province', 'zip_code', 'country']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    readonly_fields = ['avatar_diplay']
    search_fields = ['user__first_name', 'user__last_name', 'city__istartswith', 'state_or_province__istartswith',
                     'country__istartswith']

    def avatar_diplay(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
        else:
            if instance.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
            elif instance.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')

    @admin.display(ordering='id')
    def user_avatar(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
        else:
            if instance.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
            elif instance.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')

    def get_queryset(self, request):
        return super().get_queryset(request) . \
            select_related('user') . \
            filter(user__is_active=True)

    def save_model(self, request, obj, form, change):
        delete_cache_with_key_prefix('profiles_list')
        delete_cache_with_key_prefix('members_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('profiles_list')
        delete_cache_with_key_prefix('members_list')
        return super().delete_queryset(request, queryset)

    class Media:
        css = {
            'all': ['userprofile/styles.css']
        }
