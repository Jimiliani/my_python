# Generated by Django 3.1.1 on 2020-09-29 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20200929_0933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='related_post',
            new_name='post',
        ),
    ]
