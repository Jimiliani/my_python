# Generated by Django 3.0.5 on 2020-08-08 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0007_friendship'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postlike',
            old_name='related_post',
            new_name='post',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='count',
        ),
        migrations.AlterField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
