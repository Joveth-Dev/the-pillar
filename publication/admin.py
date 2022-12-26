# from django.utils import timezone
from datetime import datetime
from django.contrib import admin, messages
from django.db.models import OuterRef, Subquery
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . cache_handler import delete_cache_with_key_prefix
from . import models
from django.core.cache import cache
# from nested_admin import NestedModelAdmin, NestedStackedInline


class MemberPositionInline(admin.StackedInline):
    autocomplete_fields = ['position']
    extra = 0
    min_num = 1
    model = models.MemberPosition
    verbose_name = 'Position'


@ admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    fields = ['display_picture', 'user', 'pen_name']
    exclude = ['date_updated']
    inlines = [MemberPositionInline]
    list_display = ['profile', 'full_name',
                    'pen_name', 'current_position', 'date_updated']
    list_filter = ['date_updated']
    list_per_page = 10
    list_select_related = ['user__profile']
    ordering = ['-user__date_joined']
    readonly_fields = ['display_picture']
    search_fields = ['user__last_name__istartswith',
                     'user__first_name__istartswith', 'pen_name__istartswith']

    def display_picture(self, instance):
        if instance.user.profile.profile_image.name != '':
            return format_html(f'<img src="{instance.user.profile.profile_image.url}" class="profile"/>')
        else:
            if instance.user.profile.sex == 'M':
                instance.user.profile.profile_image = 'userprofile/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.profile.profile_image.url}" class="profile"/>')
            elif instance.user.profile.sex == 'F':
                instance.user.profile.profile_image = 'userprofile/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.profile.profile_image.url}" class="profile"/>')

    @admin.display(ordering='id')
    def profile(self, instance):
        if instance.user.profile.profile_image.name != '':
            return format_html(f'<img src="{instance.user.profile.profile_image.url}" class="profile_icon"/>')
        else:
            if instance.user.profile.sex == 'M':
                instance.user.profile.profile_image = 'userprofile/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.profile.profile_image.url}" class="profile_icon"/>')
            elif instance.user.profile.sex == 'F':
                instance.user.profile.profile_image = 'userprofile/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.profile.profile_image.url}" class="profile_icon"/>')

    @ admin.display(ordering='user__last_name')
    def full_name(self, member):
        return member.user.get_full_name()

    @ admin.display(ordering='current_position')
    def current_position(self, member):
        return member.current_position

    def get_queryset(self, request):
        subquery = models.MemberPosition.objects.select_related('position').filter(
            member_id=OuterRef('pk')).order_by('-datetime').values('position__title')[:1]
        return super().get_queryset(request). \
            prefetch_related('memberposition_set'). \
            annotate(current_position=Subquery(subquery))

    def save_model(self, request, obj, form, change):
        print(cache.keys('*'))
        delete_cache_with_key_prefix('members_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('members_list')
        return super().delete_queryset(request, queryset)

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


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    fields = ['announcement_img']
    list_display = ['id', 'posted_by', 'announcement_img',
                    'thumbnail', 'date_created']
    list_filter = ['date_created']
    list_per_page = 10
    list_select_related = ['member__user']
    ordering = ['date_created']
    search_fields = ['id']

    @admin.display(ordering='announcement_img')
    def thumbnail(self, announcement: models.Announcement):
        return format_html(f'<img src="{announcement.announcement_img.url}" class="announcement"/>')

    @admin.display(ordering='member')
    def posted_by(self, announcement: models.Announcement):
        return announcement.member

    def save_model(self, request, obj, form, change):
        obj.member = request.user.member
        return super().save_model(request, obj, form, change)

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

    def thumbnail(self, instance):
        if instance.image_for_thumbnail.name != '':
            return format_html(f'<img src="{instance.image_for_thumbnail.url}" class="thumbnail"/>')
        return ''


@ admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    actions = ['approve', 'disapprove', 'disable_display', 'enable_display']
    fields = ['member', 'volume_number', 'issue_number',
              'category', 'description', 'is_approved', 'is_enabled']
    inlines = [IssueFileInline]
    list_display = ['id', 'volume_number', 'issue_number', 'category', 'no_of_articles',
                    'uploaded_by', 'date_published', 'date_created', 'date_updated', 'is_approved', 'is_enabled']
    list_editable = ['category']
    list_filter = ['category', IsApprovedFilter,
                   IsEnabledFilter, 'date_published', 'date_created', 'date_updated']
    list_per_page = 10
    list_select_related = ['member__user', 'issuefile']
    ordering = ['date_created']
    readonly_fields = ['member']
    search_fields = ['id', 'no_of_articles', 'volume_number', 'issue_number',
                     'member__user__last_name__istartswith', 'member__user__first_name__istartswith']

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
        updated_issue_count = queryset.update(
            is_approved=True, date_published=datetime.now())
        self.message_user(
            request,
            f'{updated_issue_count} issues were successfully updated.'
        )
        delete_cache_with_key_prefix('issues_list')

    @admin.action(description='Reject selected issues')
    def disapprove(self, request, queryset):
        updated_issue_count = queryset.update(
            is_approved=False, date_published=None)
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
        if obj.is_approved:
            obj.date_published = datetime.now()
        else:
            obj.date_published = None
        delete_cache_with_key_prefix('issues_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('issues_list')
        return super().delete_queryset(request, queryset)

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
              'category', 'body', 'is_approved', 'is_enabled']
    inlines = [ArticleImageInline]
    list_display = ['id', 'issue', 'title_or_headline', 'author', 'pen_name',
                    'category', 'date_published', 'date_created', 'date_updated', 'is_approved', 'is_enabled']
    list_filter = ['category', IsApprovedFilter,
                   IsEnabledFilter, 'date_published', 'date_created', 'date_updated']
    list_per_page = 10
    list_select_related = ['issue', 'member__user']
    ordering = ['date_created']
    prepopulated_fields = {
        'slug': ['title_or_headline']
    }
    readonly_fields = ['member']
    search_fields = ['id', 'issue__issue_number', 'title_or_headline__istartswith', 'member__user__last_name__istartswith',
                     'member__user__first_name__istartswith', 'member__pen_name__istartswith']

    @admin.display(ordering='issue_id__volume_number')
    def volume(self, article):
        return article.issue.volume_number

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
        updated_count = queryset.update(
            is_approved=True, date_published=datetime.now())
        self.message_user(
            request,
            f'{updated_count} articles were successfully updated.'
        )
        delete_cache_with_key_prefix('articles_list')

    @admin.action(description='Reject selected articles')
    def disapprove(self, request, queryset):
        updated_count = queryset.update(is_approved=False, date_published=None)
        self.message_user(
            request,
            f'{updated_count} articles were successfully updated.'
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

    @admin.action(description='Enable display of selected articles')
    def enable_display(self, request, queryset):
        updated_display = queryset.update(is_enabled=True)
        self.message_user(
            request,
            f'{updated_display} articles were successfully enabled.'
        )
        delete_cache_with_key_prefix('articles_list')

    def save_model(self, request, obj, form, change):
        obj.member = request.user.member
        if obj.is_approved:
            obj.date_published = datetime.now()
        else:
            obj.date_published = None
        delete_cache_with_key_prefix('articles_list')
        return super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('articles_list')
        return super().delete_queryset(request, queryset)

    class Media:
        css = {
            'all': ['publication/styles.css']
        }
