# Generated by Django 3.1.1 on 2020-09-29 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_message_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile'),
        ),
    ]