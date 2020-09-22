# Generated by Django 3.1.1 on 2020-09-22 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepost',
            name='like',
            field=models.ManyToManyField(related_name='like', to='userprofile.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/pictures/default.png', upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='profilepost',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='userprofile.profile'),
        ),
        migrations.DeleteModel(
            name='PostLike',
        ),
    ]
