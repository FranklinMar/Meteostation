# Generated by Django 4.1 on 2023-03-01 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_region_datas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='datas',
            field=models.ManyToManyField(blank=True, to='main.data'),
        ),
    ]