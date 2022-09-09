# Generated by Django 4.1 on 2022-09-03 07:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_data_weather_code_delete_weathercode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='cloud_amount',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Кількість хмар'),
        ),
        migrations.AlterField(
            model_name='data',
            name='lower_cloud_limit',
            field=models.IntegerField(null=True, verbose_name='Нижня межа хмарності'),
        ),
    ]
