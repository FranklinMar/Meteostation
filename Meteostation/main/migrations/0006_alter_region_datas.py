# Generated by Django 4.1 on 2023-03-01 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_region_coords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='datas',
            field=models.ManyToManyField(null=True, to='main.data'),
        ),
    ]
