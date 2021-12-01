from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone
import sys


# Create your models here.
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length = 255, verbose_name = 'Категорія')
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_inf', kwargs = {'slug': self.slug})

    def get_fields_for_filter_in_templates(self):
        return ProductFeatures.objects.filter(category=self, use_in_filter=True).prefetch_related('category').value('feature_kod', 'filter_measure', 'feature_name', 'filter_type')

class Product(models.Model):

    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = 'Категорія')
    title = models.CharField(max_length = 255, verbose_name = 'Назва')
    slug = models.SlugField(unique = True)
    image = models.ImageField(verbose_name = 'Зображення')
    description = models.TextField(verbose_name = 'Опис', null = True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name = 'Ціна')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_inf', kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     image = self.image
    #     img = Image.open(image)
    #     new_img = img.convert('RGB')
    #     resized_new_image = new_img.resize((200, 200), Image.ANTIALIAS)
    #     filestream = BytesIO()
    #     resized_new_image.save(filestream, 'JPEG', quality = 90)
    #     filestream.seek(0)
    #     name = '{}.{}'.format(*self.image.name.split('.'))
    #     self.image = InMemoryUploadedFile(filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None)
    #     super().save(*args, **kwargs)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete = models.CASCADE, verbose_name = 'Покупець')
    cart = models.ForeignKey('Cart', on_delete = models.CASCADE, verbose_name = 'Кошик', related_name = 'related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default = 1)
    general_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name = 'Загальна ціна')

    def __str__(self):
        return "Продукт: {}".format(self.product.title) 

    def save(self, *args, **kwargs):
        self.general_price = self.number * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null = True, on_delete = models.CASCADE, verbose_name = 'Власник')
    products = models.ManyToManyField(CartProduct, blank = True, related_name = 'related_cart')
    general_products = models.PositiveIntegerField(default = 0)
    general_price = models.DecimalField(max_digits=9, default = 0, decimal_places=2, verbose_name = 'Загальна ціна')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name = 'Номер телефона', null = True, blank = True)
    address = models.CharField(max_length=200, verbose_name = 'Адреса', null=True, blank=True)
    orders = models.ManyToManyField('Order', related_name='related_customer', verbose_name='Замовлення покупця')

    def __str__(self):
        return "Покупець: {} {}".format(self.user.first_name, self.user.last_name)

class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progres'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення обробляється'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконане')
    )

    BUYING_SELF = 'self'
    BUYING_DELIVERY = 'delivery'

    BUYING_CHOICES = (
        (BUYING_SELF, 'Самовивіз'),
        (BUYING_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, related_name='related_orders', on_delete = models.CASCADE, verbose_name = 'Покупець')
    first_name = models.CharField(max_length = 250, verbose_name = "Ім'я")
    last_name = models.CharField(max_length=250, verbose_name = 'Прізвище')
    phone = models.CharField(max_length=20, verbose_name = 'Мобільний номер')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кошик')
    address = models.CharField(max_length=500, verbose_name = 'Адреса', null = True, blank = True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW)
    buying = models.CharField(max_length=50, choices=BUYING_CHOICES, default=BUYING_SELF)
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар до замовлення(не обов'язково)")
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')
    order_date = models.DateField(default=timezone.now, verbose_name='Дата отримання замовлення')

    def __str__(self):
        return str(self.id)

class ProductFeatures(models.Model):

    # RADIOBTN = "radio"
    CHECKBOX = "checkbox"

    # FILTER_TYPE_CHOICES = ((RADIOBTN, 'Радіокнопка'), (CHECKBOX, 'Прапорець'))

    feature_kod = models.CharField(max_length=250, verbose_name='Код характеристик')
    feature_name = models.CharField(max_length=250, verbose_name='Назва характеристик')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія')
    postfix = models.CharField(max_length=50, null=True, blank=True, verbose_name='Постфікс')
    filter_use = models.BooleanField(default=False, verbose_name='Використовувати для фільтра')
    # filter_type = models.CharField(max_length=50, default=CHECKBOX, choices=FILTER_TYPE_CHOICES)
    filter_type = models.CharField(max_length=50, default=CHECKBOX,)
    filter_measure  = models.CharField(max_length=50, verbose_name='Одиниця виміру')

    def __str__(self):
        return f'Категорія - "{self.category.name}" | Характеристика - "{self.feature_name}"'

class ProductFeaturesValidators(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія')
    feature = models.ForeignKey(ProductFeatures, on_delete=models.CASCADE, verbose_name='Характеристика', null=True, blank=True)
    feature_value = models.CharField(max_length=250, verbose_name='Значення характеристики', unique=True, null=True, blank=True)

    def __str__(self):
        if not self.feature:
            return f'Характеристика не обрана!'
        return f'Валідація прошла успішно!'