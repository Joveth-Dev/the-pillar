# Generated by Django 4.1.5 on 2023-01-24 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0030_remove_issue_is_active_member_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='try_lng',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]