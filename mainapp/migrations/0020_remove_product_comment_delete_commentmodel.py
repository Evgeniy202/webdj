# Generated by Django 4.0.1 on 2022-03-30 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_commentmodel_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='comment',
        ),
        migrations.DeleteModel(
            name='CommentModel',
        ),
    ]