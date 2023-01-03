from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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
    list_display = ['picture', 'username', 'email', 'first_name',
                    'middle_initial', 'last_name', 'is_staff', 'is_active']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": (
            'display_picture', "first_name", 'middle_initial', "last_name", "email")}),
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

    readonly_fields = ['display_picture']
    list_per_page = 10
    list_select_related = ['profile']

    def display_picture(self, instance):
        if instance.profile.profile_image.name != '':
            return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile"/>')
        else:
            if instance.profile.sex == 'M':
                instance.profile.profile_image = 'userprofile/images/default_male.jpg'
                return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile"/>')
            elif instance.profile.sex == 'F':
                instance.profile.profile_image = 'userprofile/images/default_female.jpg'
                return format_html(f'<img src="{instance.profile.profile_image.url}" class="profile"/>')

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

    class Media:
        css = {
            'all': ['core/styles.css']
        }
