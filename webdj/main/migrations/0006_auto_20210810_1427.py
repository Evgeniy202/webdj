# Generated by Django 2.2.20 on 2021-08-10 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210810_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soft_baits',
            name='edible',
            field=models.BooleanField(default=True, verbose_name='Їстівна'),
        ),
    ]
