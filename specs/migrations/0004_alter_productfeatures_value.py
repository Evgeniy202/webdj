# Generated by Django 4.0.1 on 2022-02-13 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0003_alter_productfeatures_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeatures',
            name='value',
            field=models.CharField(max_length=255, verbose_name='Значення'),
        ),
    ]
