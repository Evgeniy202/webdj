# Generated by Django 4.0.1 on 2022-03-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Активність'),
        ),
    ]
