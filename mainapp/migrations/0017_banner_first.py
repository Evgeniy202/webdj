# Generated by Django 4.0.1 on 2022-03-27 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_banner_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='first',
            field=models.BooleanField(default=False, verbose_name='Перший в слайдері'),
        ),
    ]
