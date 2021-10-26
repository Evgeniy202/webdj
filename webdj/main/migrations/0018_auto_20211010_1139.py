# Generated by Django 2.2.20 on 2021-10-10 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_order_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Зображення')),
                ('description', models.TextField(null=True, verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ціна')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Category', verbose_name='Категорія')),
            ],
        ),
        migrations.RemoveField(
            model_name='coils',
            name='category',
        ),
        migrations.RemoveField(
            model_name='corbs_and_lines',
            name='category',
        ),
        migrations.RemoveField(
            model_name='feeders',
            name='category',
        ),
        migrations.RemoveField(
            model_name='fishing_accessories',
            name='category',
        ),
        migrations.RemoveField(
            model_name='groundbaits_ozzles',
            name='category',
        ),
        migrations.RemoveField(
            model_name='hooks',
            name='category',
        ),
        migrations.RemoveField(
            model_name='leashes',
            name='category',
        ),
        migrations.RemoveField(
            model_name='rods',
            name='category',
        ),
        migrations.RemoveField(
            model_name='soft_baits',
            name='category',
        ),
        migrations.RemoveField(
            model_name='spinners',
            name='category',
        ),
        migrations.RemoveField(
            model_name='wobblers',
            name='category',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='object_id',
        ),
        migrations.DeleteModel(
            name='cargo',
        ),
        migrations.DeleteModel(
            name='coils',
        ),
        migrations.DeleteModel(
            name='corbs_and_lines',
        ),
        migrations.DeleteModel(
            name='feeders',
        ),
        migrations.DeleteModel(
            name='fishing_accessories',
        ),
        migrations.DeleteModel(
            name='groundbaits_ozzles',
        ),
        migrations.DeleteModel(
            name='hooks',
        ),
        migrations.DeleteModel(
            name='leashes',
        ),
        migrations.DeleteModel(
            name='rods',
        ),
        migrations.DeleteModel(
            name='soft_baits',
        ),
        migrations.DeleteModel(
            name='spinners',
        ),
        migrations.DeleteModel(
            name='wobblers',
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(default=1, on_delete='CASCADE', to='main.Product', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]