# Generated by Django 3.0.5 on 2020-08-03 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_greenleafuserprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='greenleafuserprofile',
            name='profile_picture',
            field=models.ImageField(default='default.png', upload_to='<django.db.models.fields.PositiveIntegerField>'),
        ),
    ]