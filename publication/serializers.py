from rest_framework import serializers
from .models import Announcement, Article, ArticleImage, Issue, IssueFile, Member


class MemberSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    sex = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    current_position = serializers.SerializerMethodField()

    def get_profile(self, member: Member):
        if member.user.profile.profile_image.name == '':
            return ''
        return member.user.profile.profile_image.url

    def get_sex(self, member: Member):
        return member.user.profile.sex

    def get_full_name(self, member: Member):
        return str(member.user.get_full_name())

    def get_current_position(self, member: Member):
        return member.current_position

    class Meta:
        model = Member
        fields = ['id', 'profile', 'full_name',
                  'sex', 'pen_name', 'current_position']


class IssueFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueFile
        fields = ['issue_id', 'file', 'image_for_thumbnail']


class IssueSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Issue
        fields = ['id', 'volume_number', 'issue_number', 'category',
                  'issue_file', 'description', 'articles_count', 'date_published', 'date_updated']
    issue_file = IssueFileSerializer(source='issuefile')
    articles_count = serializers.IntegerField(read_only=True)


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['id', 'image', 'image_caption']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'pen_name', 'issue', 'category', 'title_or_headline',
                  'article_images', 'body', 'date_published', 'date_updated']
    author = serializers.SerializerMethodField()
    pen_name = serializers.SerializerMethodField()
    issue = serializers.HyperlinkedRelatedField(
        queryset=Issue.objects.all(),
        view_name='issues-detail'
    )
    article_images = ArticleImageSerializer(many=True)

    def get_author(self, article: Article):
        return str(article.member.user.get_full_name())

    def get_pen_name(self, article: Article):
        return str(article.member.pen_name)


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'announcement_img', 'member', 'date_created']
