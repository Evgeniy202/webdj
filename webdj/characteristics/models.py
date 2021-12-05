from django.db import models

class CharacteristicCategory(models.Model):

    category = models.ForeignKey('main.Category', verbose_name='Категорія', on_delete=models.CASCADE)