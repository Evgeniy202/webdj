# Generated by Django 4.0.1 on 2022-02-20 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_product_img1_product_img2_product_img3_product_img4_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img1',
            field=models.ImageField(null=True, upload_to='', verbose_name="Додаткове зображення (не обов'язково)"),
        ),
    ]
