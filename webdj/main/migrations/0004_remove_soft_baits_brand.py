# Generated by Django 2.2.20 on 2021-08-10 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210803_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soft_baits',
            name='brand',
        ),
    ]
