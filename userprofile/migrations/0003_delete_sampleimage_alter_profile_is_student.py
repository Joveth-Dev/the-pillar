# Generated by Django 4.1.3 on 2022-11-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_alter_profile_is_student'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SampleImage',
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]
