# Generated by Django 4.1.3 on 2022-11-20 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_alter_profile_user'),
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='userprofile.profile'),
        ),
    ]
