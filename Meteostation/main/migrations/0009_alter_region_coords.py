# Generated by Django 4.1 on 2023-03-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_region_offset_x_region_offset_y'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='coords',
            field=models.TextField(default='', max_length=4000, verbose_name='Координати мапи'),
        ),
    ]
