# Generated by Django 4.2.6 on 2023-11-18 09:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game_engine', '0002_alter_userprofile_game_mode'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='display_name',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together={('user', 'game_mode', 'display_name')},
        ),
    ]
