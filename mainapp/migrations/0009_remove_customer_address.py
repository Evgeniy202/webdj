# Generated by Django 4.0.1 on 2022-02-20 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_remove_order_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
    ]