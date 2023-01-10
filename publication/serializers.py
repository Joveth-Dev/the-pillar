from rest_framework import serializers
from .models import Announcement, Article, ArticleImage, Issue, IssueFile, Member, Banner


class MemberSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    sex = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    current_position = serializers.SerializerMethodField()

    def get_avatar(self, member: Member):
        if member.user.avatar.name == '':
            return ''
        return member.user.avatar.url

    def get_sex(self, member: Member):
        return member.user.profile.sex

    def get_full_name(self, member: Member):
        return str(member.user.get_full_name())

    def get_current_position(self, member: Member):
        return member.current_position

    class Meta:
        model = Member
        fields = ['id', 'avatar', 'full_name',
                  'sex', 'pen_name', 'current_position']


class IssueFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueFile
        fields = ['issue_id', 'file', 'image_for_thumbnail']


class IssueSerializer(serializers.ModelSerializer):
    issue_file = IssueFileSerializer(source='issuefile')
    articles_count = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Issue
        fields = ['id', 'volume_number', 'issue_number', 'category',
                  'issue_file', 'description', 'articles_count', 'date_published', 'date_updated']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['id', 'image', 'image_caption']


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    pen_name = serializers.SerializerMethodField()
    issue = serializers.HyperlinkedRelatedField(
        queryset=Issue.objects.all(),
        view_name='issues-detail'
    )
    article_images = ArticleImageSerializer(many=True)

    class Meta:
        model = Article
        fields = ['id', 'author', 'pen_name', 'issue', 'category', 'title_or_headline',
                  'article_images', 'body', 'date_published', 'date_updated']

    def get_author(self, article: Article):
        return str(article.member.user.get_full_name())

    def get_pen_name(self, article: Article):
        return str(article.member.pen_name)


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'announcement_img', 'member', 'date_created']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'member', 'image']
