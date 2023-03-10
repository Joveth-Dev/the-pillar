# Generated by Django 4.1.3 on 2022-11-15 14:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import publication.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title_or_headline', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('category', models.CharField(choices=[('N', 'News'), ('NF', 'News Feature'), ('F', 'Feature'), (
                    'O', 'Opinion'), ('C', 'Culture'), ('E', 'Editorial'), ('CL', 'Column')], max_length=2)),
                ('body', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('volume_number', models.PositiveIntegerField(
                    validators=[django.core.validators.MinValueValidator(1)])),
                ('issue_number', models.PositiveIntegerField(
                    validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('LF', 'Literary Folio'), (
                    'T', 'Tabloid'), ('M', 'Magazine'), ('N', 'Newsletter')], max_length=2)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('pen_name', models.CharField(max_length=85)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=27)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IssueFile',
            fields=[
                ('issue', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                 primary_key=True, serialize=False, to='publication.issue')),
                ('file', models.FileField(upload_to='publication/files', validators=[
                 django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('image_for_thumbnail', models.ImageField(upload_to='publication/files/thumbnails',
                 validators=[publication.validators.validate_image_size])),
            ],
        ),
        migrations.CreateModel(
            name='MemberPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='publication.member')),
                ('position', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.CASCADE, to='publication.position')),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='member',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='publication.member'),
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=255, upload_to='publication/images',
                 validators=[publication.validators.validate_image_size])),
                ('image_caption', models.CharField(blank=True, max_length=255)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='article_images', to='publication.article')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='articles', to='publication.issue'),
        ),
        migrations.AddField(
            model_name='article',
            name='member',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='publication.member'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement_img', models.ImageField(
                    max_length=255, upload_to='announcement/images')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(
                    on_delete=django.db.models.deletion.DO_NOTHING, to='publication.member')),
            ],
        ),
    ]
