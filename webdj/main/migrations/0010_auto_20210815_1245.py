# Generated by Django 2.2.20 on 2021-08-15 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210815_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='for_anonymos',
            new_name='for_anonymos_user',
        ),
    ]
