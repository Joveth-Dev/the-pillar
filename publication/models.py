from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from .validators import validate_image_size


class Member(models.Model):
    pen_name = models.CharField(max_length=85)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.get_full_name()

    def get_pen_name(self):
        return self.pen_name

    def delete(self, *args, **kwargs):
        # set is_active to False instead of deleting
        self.is_active = False
        super(Member, self).save(*args, **kwargs)


class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['id']


class MemberPosition(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    date_assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.position.title


class Issue(models.Model):
    LITERARY_FOLIO = 'LF'
    TABLOID = 'T'
    SPORTS_MAGAZINE = 'SM'
    NEWSLETTER = 'N'

    CATEGORY_CHOICES = [
        (LITERARY_FOLIO, 'Literary Folio'),
        (TABLOID, 'Tabloid'),
        (SPORTS_MAGAZINE, 'Sports Magazine'),
        (NEWSLETTER, 'Newsletter')
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    volume_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)])
    issue_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)])
    description = models.TextField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateField()
    is_approved = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.issue_number)


class IssueFile(models.Model):
    issue = models.OneToOneField(
        Issue,
        on_delete=models.CASCADE,
        primary_key=True)
    file = models.FileField(
        upload_to='publication/files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    image_for_thumbnail = models.ImageField(
        upload_to='publication/files/thumbnails',
        validators=[validate_image_size])

    def __str__(self) -> str:
        file_name = f'File name: {self.file.name.replace("publication/files/", "")}'
        return file_name


class Article(models.Model):
    NEWS = 'N'
    NEWS_FEATURE = 'NF'
    FEATURE = 'F'
    OPINION = 'O'
    CULTURE = 'C'
    EDITORIAL = 'E'
    COLUMN = 'CL'

    CATEGORY_CHOICES = [
        (NEWS, 'News'),
        (NEWS_FEATURE, 'News Feature'),
        (FEATURE, 'Feature'),
        (OPINION, 'Opinion'),
        (CULTURE, 'Culture'),
        (EDITORIAL, 'Editorial'),
        (COLUMN, 'Column')
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, null=True, blank=True, related_name='articles')
    title_or_headline = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateField()
    is_approved = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'"{self.title_or_headline}"'


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='article_images')
    image = models.ImageField(
        upload_to='publication/images',
        blank=True,
        validators=[validate_image_size])
    image_caption = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        image_name = f'File name: {self.image.name.replace("publication/images/", "")}'
        return image_name


class Announcement(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    announcement_img = models.ImageField(
        upload_to='announcement/images', max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)


class Banner(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='publication/banners',
        validators=[validate_image_size])
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
