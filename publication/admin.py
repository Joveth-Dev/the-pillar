from django.contrib import admin, messages
from django.db.models import OuterRef, Subquery
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . cache_handler import delete_cache_with_key_prefix
from . import models

# from nested_admin import NestedModelAdmin, NestedStackedInline

from django.contrib.auth.models import Permission
admin.site.register(Permission)


class MemberPositionInline(admin.StackedInline):
    autocomplete_fields = ['position']
    extra = 0
    min_num = 1
    model = models.MemberPosition
    verbose_name = 'Position'


@ admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    fields = ['avatar_diplay', 'user', 'pen_name', 'is_active']
    exclude = ['date_updated']
    inlines = [MemberPositionInline]
    list_display = ['user_avatar', 'full_name',
                    'pen_name', 'current_position', 'date_updated', 'is_active']
    list_filter = ['date_updated', 'is_active']
    list_per_page = 10
    list_select_related = ['user__profile']
    ordering = ['-user__date_joined']
    readonly_fields = ['avatar_diplay']
    search_fields = ['user__last_name__istartswith',
                     'user__first_name__istartswith', 'pen_name__istartswith']

    def avatar_diplay(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
        else:
            if instance.user.profile.sex == 'N':
                instance.user.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
            elif instance.user.profile.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
            elif instance.user.profile.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')

    @admin.display(ordering='id')
    def user_avatar(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
        else:
            if instance.user.profile.sex == 'N':
                instance.user.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
            elif instance.user.profile.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
            elif instance.user.profile.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')

    @admin.display(ordering='user__last_name')
    def full_name(self, member):
        return member.user.get_full_name()

    @ admin.display(ordering='current_position')
    def current_position(self, member):
        return member.current_position

    def get_queryset(self, request):
        subquery = models.MemberPosition.objects.select_related('position').filter(
            member_id=OuterRef('pk')).order_by('-date_assigned').values('position__title')[:1]
        return super().get_queryset(request). \
            select_related('user') . \
            filter(user__is_active=True) . \
            prefetch_related('memberposition_set'). \
            annotate(current_position=Subquery(subquery))

    def save_model(self, request, obj, form, change):
        delete_cache_with_key_prefix('members_list')
        return super().save_model(request, obj, form, change)

    # SET MEMBER TO INACTIVE INSTEAD OF DELETING
    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('members_list')
        queryset.update(is_active=False)
    # ========================================

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


@ admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'position']
    search_fields = ['title__istartswith']

    @admin.display(ordering='title')
    def position(self, position):
        return position.title


@admin.register(models.MemberPosition)
class MemberPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'position', 'date_assigned']


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    actions = ['approve', 'disapprove', 'disable_display', 'enable_display']
    fields = ['announcement_img', 'is_approved']
    list_display = ['thumbnail', 'announcement_img',
                    'created_by', 'date_created', 'is_approved']
    list_filter = ['is_approved', 'member', 'date_created']
    list_per_page = 10
    list_select_related = ['member__user']
    ordering = ['date_created']

    @admin.display(ordering='id')
    def thumbnail(self, announcement: models.Announcement):
        return format_html(f'<img src="{announcement.announcement_img.url}" class="announcement"/>')

    @admin.display(ordering='member')
    def created_by(self, announcement: models.Announcement):
        return announcement.member

    @admin.action(description='Approve selected issues')
    def approve(self, request, queryset):
        updated_issue_count = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated_issue_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('announcements_list')

    @admin.action(description='Disapprove selected issues')
    def disapprove(self, request, queryset):
        updated_issue_count = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated_issue_count} issues and were successfully updated.'
        )
        delete_cache_with_key_prefix('announcements_list')

    @admin.action(description='Disable display of selected issues')
    def disable_display(self, request, queryset):
        updated_issues_count = queryset.update(is_enabled=False)
        self.message_user(
            request,
            f'{updated_issues_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('announcements_list')

    @admin.action(description='Enable display of selected issues')
    def enable_display(self, request, queryset):
        updated_issues_count = queryset.update(is_enabled=True)
        self.message_user(
            request,
            f'{updated_issues_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('announcements_list')

    def save_model(self, request, obj, form, change):
        obj.member = request.user.member
        delete_cache_with_key_prefix('announcements_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('announcements_list')
        return super().delete_queryset(request, queryset)

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


class IsEnabledFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_enabled' field"""
    title = 'display'
    parameter_name = 'display'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Enabled'),
            ('No', 'Disabled')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_enabled=True)
        elif self.value() == 'No':
            return queryset.filter(is_enabled=False)


class IsApprovedFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_active' field"""
    title = 'approval status'
    parameter_name = 'is_approved'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'True'),
            ('No', 'False')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_approved=True)
        elif self.value() == 'No':
            return queryset.filter(is_approved=False)


# class ArticleImageNestedInline(NestedStackedInline):
#     extra = 1
#     max_num = 3
#     model = models.ArticleImage
#     readonly_fields = ['thumbnail']

#     def thumbnail(self, instance):
#         if instance.image.name != '':
#             return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
#         return ''


# class ArticleInline(admin.StackedInline):
#     # inlines = [ArticleImageNestedInline]
#     extra = 0
#     model = models.Article


class IssueFileInline(admin.StackedInline):
    model = models.IssueFile
    readonly_fields = ['thumbnail']
    verbose_name_plural = 'Issue'
    min_num = 1
    max_num = 1

    def thumbnail(self, instance):
        if instance.image_for_thumbnail.name != '':
            return format_html(f'<img src="{instance.image_for_thumbnail.url}" class="thumbnail"/>')
        return ''


@ admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    actions = ['approve', 'disapprove', 'disable_display', 'enable_display']
    fields = ['member', 'volume_number', 'issue_number', 'date_published',
              'category', 'description']  # , 'is_approved', 'is_enabled'
    inlines = [IssueFileInline]
    list_display = ['id', 'volume_number', 'issue_number', 'category', 'uploaded_by', 'date_published',
                    'date_created', 'date_updated', 'no_of_articles', 'is_approved', 'is_enabled']
    list_filter = ['category', IsApprovedFilter,
                   IsEnabledFilter, 'date_published', 'date_created', 'date_updated']
    list_per_page = 10
    list_select_related = ['member__user', 'issuefile']
    ordering = ['-date_created']
    readonly_fields = ['member']
    search_fields = ['id__exact', 'volume_number__contains', 'issue_number__contains', 'description__icontains',
                     'member__user__last_name__istartswith', 'member__user__first_name__istartswith', 'member__pen_name__istartswith']

    @admin.display(ordering='member')
    def uploaded_by(self, issue):
        return issue.member

    @admin.display(ordering='no_of_articles')
    def no_of_articles(self, issue):
        url = (
            reverse('admin:publication_article_changelist')
            + '?'
            + urlencode({
                'issue__id': str(issue.id)
            }))
        return format_html('<a href={}>{}</a>', url, issue.no_of_articles)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(no_of_articles=Count('articles'))

    @admin.action(description='Approve selected issues')
    def approve(self, request, queryset):
        updated_issue_count = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated_issue_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('issues_list')

    @admin.action(description='Disapprove selected issues')
    def disapprove(self, request, queryset):
        updated_issue_count = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated_issue_count} issues and were successfully updated.'
        )
        delete_cache_with_key_prefix('issues_list')

    @admin.action(description='Disable display of selected issues')
    def disable_display(self, request, queryset):
        updated_issues_count = queryset.update(is_enabled=False)
        self.message_user(
            request,
            f'{updated_issues_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('issues_list')

    @admin.action(description='Enable display of selected issues')
    def enable_display(self, request, queryset):
        updated_issues_count = queryset.update(is_enabled=True)
        self.message_user(
            request,
            f'{updated_issues_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('issues_list')

    def save_model(self, request, obj, form, change):
        obj.member = request.user.member
        delete_cache_with_key_prefix('issues_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('issues_list')
        return super().delete_queryset(request, queryset)

    def get_actions(self, request):
        actions = super().get_actions(request)
        # for removing approval and display action if no permission
        if not request.user.has_perms(['publication.can_approve_issue',
                                       'publication.can_disapprove_issue',
                                       'publication.can_enable_issue',
                                       'publication.can_disable_issue']):
            del actions['approve']
            del actions['disapprove']
            del actions['enable_display']
            del actions['disable_display']
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


class IsApprovedFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_approved' field"""
    title = 'approval status'
    parameter_name = 'is_approved'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Approved'),
            ('No', 'Not Approved')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_approved=True)
        elif self.value() == 'No':
            return queryset.filter(is_approved=False)


class IsEnabledFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_enabled' field"""
    title = 'Display'
    parameter_name = 'display'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Enabled'),
            ('No', 'Disabled')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_enabled=True)
        elif self.value() == 'No':
            return queryset.filter(is_enabled=False)


class ArticleImageInline(admin.StackedInline):
    extra = 0
    max_num = 3
    model = models.ArticleImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return 'No Image Yet'


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = ['approve', 'disapprove', 'disable_display', 'enable_display']
    autocomplete_fields = ['issue']
    fields = ['member', 'issue', 'title_or_headline', 'slug',
              'date_published', 'category', 'body']  # , 'is_approved', 'is_enabled'
    inlines = [ArticleImageInline]
    list_display = ['id', 'issue', 'title_or_headline', 'author', 'pen_name',
                    'category', 'date_published', 'date_created', 'date_updated', 'is_approved', 'is_enabled']
    list_filter = ['category', IsApprovedFilter,
                   IsEnabledFilter, 'date_published', 'date_created', 'date_updated']
    list_per_page = 10
    list_select_related = ['issue', 'member__user']
    ordering = ['-date_created']
    prepopulated_fields = {
        'slug': ['title_or_headline']
    }
    readonly_fields = ['member']
    search_fields = ['id__exact', 'title_or_headline__icontains', 'member__user__last_name__istartswith',
                     'member__user__first_name__istartswith', 'member__pen_name__istartswith', 'body__icontains']

    @admin.display(ordering='member')
    def author(self, article):
        return article.member

    @admin.display(ordering='member__pen_name')
    def pen_name(self, article):
        if article.category == 'CL':
            return str(article.member.pen_name).upper()
        return str(article.member.pen_name)

    @admin.action(description='Approve selected articles')
    def approve(self, request, queryset):
        updated_count = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated_count} articles were successfully updated.'
        )
        delete_cache_with_key_prefix('articles_list')

    @admin.action(description='Disapprove selected articles')
    def disapprove(self, request, queryset):
        updated_count = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated_count} articles were successfully updated.'
        )
        delete_cache_with_key_prefix('articles_list')

    @admin.action(description='Enable display of selected articles')
    def enable_display(self, request, queryset):
        updated_display = queryset.update(is_enabled=True)
        self.message_user(
            request,
            f'{updated_display} articles were successfully enabled.'
        )
        delete_cache_with_key_prefix('articles_list')

    @admin.action(description='Disable display of selected articles')
    def disable_display(self, request, queryset):
        updated_display = queryset.update(is_enabled=False)
        self.message_user(
            request,
            f'{updated_display} articles were successfully disabled.',
            messages.ERROR
        )
        delete_cache_with_key_prefix('articles_list')

    def save_model(self, request, obj, form, change):
        obj.member = request.user.member
        delete_cache_with_key_prefix('articles_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('articles_list')
        return super().delete_queryset(request, queryset)

    def get_actions(self, request):
        actions = super().get_actions(request)
        # for removing approval and display action if no permission
        if not request.user.has_perms(['publication.can_approve_article',
                                       'publication.can_disapprove_article',
                                       'publication.can_enable_article',
                                       'publication.can_disable_article']):
            del actions['approve']
            del actions['disapprove']
            del actions['enable_display']
            del actions['disable_display']
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    actions = ['approve', 'disapprove', 'disable_display', 'enable_display']
    fields = ['image', 'is_approved']
    list_display = ['thumbnail', 'image',
                    'created_by', 'is_approved', 'date_created']
    list_filter = ['is_approved', 'member', 'date_created']
    readonly_fields = ['member']
    search_fields = ['member__']

    @admin.display(ordering='id')
    def thumbnail(self, banner: models.Banner):
        return format_html(f'<img src="{banner.image.url}" class="announcement"/>')

    @admin.display(ordering='member')
    def created_by(self, banner: models.Banner):
        return banner.member

    @admin.action(description='Approve selected issues')
    def approve(self, request, queryset):
        updated_issue_count = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated_issue_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('banners_list')

    @admin.action(description='Disapprove selected issues')
    def disapprove(self, request, queryset):
        updated_issue_count = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated_issue_count} issues and were successfully updated.'
        )
        delete_cache_with_key_prefix('banners_list')

    @admin.action(description='Disable display of selected issues')
    def disable_display(self, request, queryset):
        updated_issues_count = queryset.update(is_enabled=False)
        self.message_user(
            request,
            f'{updated_issues_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('banners_list')

    @admin.action(description='Enable display of selected issues')
    def enable_display(self, request, queryset):
        updated_issues_count = queryset.update(is_enabled=True)
        self.message_user(
            request,
            f'{updated_issues_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('banners_list')

    def save_model(self, request, obj, form, change):
        obj.member = request.user.member
        delete_cache_with_key_prefix('banners_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('benners_list')
        return super().delete_queryset(request, queryset)

    class Media:
        css = {
            'all': ['publication/styles.css']
        }
