# Generated by Django 4.1.5 on 2023-01-07 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_remove_profile_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_image',
        ),
    ]
