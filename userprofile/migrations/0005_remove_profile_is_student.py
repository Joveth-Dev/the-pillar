# Generated by Django 4.1.4 on 2022-12-20 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_student',
        ),
    ]
