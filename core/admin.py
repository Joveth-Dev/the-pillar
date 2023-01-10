from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # SET USER TO INACTIVE INSTEAD OF DELETING
    def delete_queryset(self, request, queryset):
        queryset.update(is_active=False)
    # ========================================

    actions = ['delete_user']
    list_display = ['user_avatar', 'username', 'email', 'first_name',
                    'middle_initial', 'last_name', 'is_staff', 'is_active']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
         "fields": ('avatar_diplay', 'avatar', "first_name", 'middle_initial', "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'last_name', 'first_name', 'middle_initial'),
            },
        ),
    )

    readonly_fields = ['avatar_diplay']
    list_per_page = 10
    list_select_related = ['profile']

    def avatar_diplay(self, instance):
        if instance.avatar.name != '':
            return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')
        else:
            if instance.profile.sex == 'N':
                instance.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')
            elif instance.profile.sex == 'M':
                instance.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')
            elif instance.profile.sex == 'F':
                instance.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')

    @admin.display(ordering='id')
    def user_avatar(self, instance):
        if instance.avatar.name != '':
            return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')
        else:
            if instance.profile.sex == 'N':
                instance.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')
            elif instance.profile.sex == 'M':
                instance.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')
            elif instance.profile.sex == 'F':
                instance.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')

    # def save_model(self, request, obj, form, change):
    #     if obj.avatar == '':
    #         if obj.profile.sex == 'N':
    #             obj.avatar = 'core/images/default_no_sex.jpg'
    #         if obj.profile.sex == 'M':
    #             obj.avatar = 'core/images/default_male.jpg'
    #         if obj.profile.sex == 'F':
    #             obj.avatar = 'core/images/default_female.jpg'
    #     return super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ['core/styles.css']
        }
