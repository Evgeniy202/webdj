# Generated by Django 4.0.1 on 2022-02-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_alter_product_img1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name="Додаткове зображення (не обов'язково)"),
        ),
    ]
