# Generated by Django 4.0.1 on 2022-03-27 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_rename_img_product_img1'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Товар в наявності'),
        ),
    ]
