# Generated by Django 3.1.1 on 2020-09-20 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('gender', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('U', 'Унисекс')], max_length=8)),
                ('materials', models.CharField(blank=True, max_length=100)),
                ('about', models.CharField(blank=True, max_length=100)),
                ('firm', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainpage.item')),
                ('count_size_XS', models.PositiveSmallIntegerField(default=0)),
                ('count_size_S', models.PositiveSmallIntegerField(default=0)),
                ('count_size_M', models.PositiveSmallIntegerField(default=0)),
                ('count_size_L', models.PositiveSmallIntegerField(default=0)),
                ('count_size_XL', models.PositiveSmallIntegerField(default=0)),
            ],
            bases=('mainpage.item',),
        ),
        migrations.CreateModel(
            name='Outwear',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainpage.item')),
                ('count_size_34_36', models.PositiveSmallIntegerField(default=0)),
                ('count_size_36_38', models.PositiveSmallIntegerField(default=0)),
                ('count_size_38_40', models.PositiveSmallIntegerField(default=0)),
                ('count_size_40_42', models.PositiveSmallIntegerField(default=0)),
                ('count_size_42_44', models.PositiveSmallIntegerField(default=0)),
                ('count_size_44_46', models.PositiveSmallIntegerField(default=0)),
                ('count_size_46_48', models.PositiveSmallIntegerField(default=0)),
                ('count_size_48_50', models.PositiveSmallIntegerField(default=0)),
                ('count_size_50_52', models.PositiveSmallIntegerField(default=0)),
            ],
            bases=('mainpage.item',),
        ),
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainpage.item')),
                ('count_size_32_34', models.PositiveSmallIntegerField(default=0)),
                ('count_size_34_36', models.PositiveSmallIntegerField(default=0)),
                ('count_size_36_38', models.PositiveSmallIntegerField(default=0)),
                ('count_size_38_40', models.PositiveSmallIntegerField(default=0)),
                ('count_size_40_42', models.PositiveSmallIntegerField(default=0)),
                ('count_size_42_44', models.PositiveSmallIntegerField(default=0)),
                ('count_size_44_46', models.PositiveSmallIntegerField(default=0)),
                ('count_size_46_48', models.PositiveSmallIntegerField(default=0)),
                ('count_size_48_50', models.PositiveSmallIntegerField(default=0)),
            ],
            bases=('mainpage.item',),
        ),
        migrations.CreateModel(
            name='Underwear',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainpage.item')),
                ('count_size_28_30', models.PositiveSmallIntegerField(default=0)),
                ('count_size_30_32', models.PositiveSmallIntegerField(default=0)),
                ('count_size_32_34', models.PositiveSmallIntegerField(default=0)),
                ('count_size_34_36', models.PositiveSmallIntegerField(default=0)),
                ('count_size_36_38', models.PositiveSmallIntegerField(default=0)),
                ('count_size_38_40', models.PositiveSmallIntegerField(default=0)),
                ('count_size_40_42', models.PositiveSmallIntegerField(default=0)),
                ('count_size_42_44', models.PositiveSmallIntegerField(default=0)),
                ('count_size_44_46', models.PositiveSmallIntegerField(default=0)),
            ],
            bases=('mainpage.item',),
        ),
    ]
