# Generated by Django 3.1.1 on 2020-09-28 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend1_agree', models.BooleanField(default=False)),
                ('friend2_agree', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('profile_picture', models.ImageField(blank=True, default='/pictures/default.png', upload_to='pictures/')),
                ('city', models.CharField(blank=True, max_length=63)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('friends', models.ManyToManyField(related_name='_profile_friends_+', through='userprofile.Friendship', to='userprofile.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_text', models.TextField(max_length=10000)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='userprofile.profile')),
                ('like', models.ManyToManyField(related_name='like', to='userprofile.Profile')),
            ],
            options={
                'ordering': ['-publication_date'],
            },
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile')),
                ('related_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profilepost')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.friendship')),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend1', to='userprofile.profile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend2', to='userprofile.profile'),
        ),
    ]
