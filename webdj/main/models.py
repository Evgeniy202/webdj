from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone
import sys


# Create your models here.
User = get_user_model()

def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]

def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs = {'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in = args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model = with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key = lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse = True)
        return products


class LatestProducts:
    objects = LatestProductsManager()

class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Грузила': 'cargo__count',
        'Котушки': 'coils__count',
        'Шнури та волосінь': 'corbs_and_lines__count',
        'Годівниці': 'feeders__count',
        'Аксесуари для риболовлі': 'fishing_accessories__count',
        'Прикорм та насадки': 'groundbaits_ozzles__count',
        'Гачки': 'hooks__count',
        'Повідці': 'leashes__count',
        'Вудилища': 'rods__count',
        "М'які приманки": 'soft_baits__count',
        'Блешні': 'spinners__count',
        'Воблери': 'wobblers__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_dropdown(self):
        models = get_models_for_count(
            'hooks', 'cargo', 'coils', 'corbs_and_lines', 'feeders', 'fishing_accessories',
            'groundbaits_ozzles', 'leashes', 'rods', 'soft_baits', 'spinners', 'wobblers'
        )
        qs = list(self.get_queryset().annotate(*models))  
        data = [dict(name = c.name, url = c.get_absolute_url(), count = getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name])) for c in qs]
        return data


class Category(models.Model):
    name = models.CharField(max_length = 255, verbose_name = 'Категорія')
    slug = models.SlugField(unique = True)
    objects = CategoryManager() 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_inf', kwargs = {'slug': self.slug})

class Product(models.Model):

    class Meta:
        abstract = True

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
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    number = models.PositiveIntegerField(default = 1)
    general_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name = 'Загальна ціна')

    def __str__(self):
        return "Продукт: {}".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.general_price = self.number * self.content_object.price
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

#Category of products

class Hooks(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    size = models.CharField(max_length=3, verbose_name = 'Розмір')
    material = models.CharField(max_length=100, verbose_name = 'Мітеріал')
    assignmant = models.CharField(max_length=200, verbose_name = 'Призначення')
    package_quantity = models.CharField(max_length=50, verbose_name = 'К-ть в упаковці(шт)')
    type = models.CharField(max_length=100, verbose_name = 'Тип')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Rods(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    construction = models.CharField(max_length=200, verbose_name = 'Конструкція')
    material = models.CharField(max_length=200, verbose_name = 'Матеріал')
    numders_sections = models.CharField(max_length=200, verbose_name = 'К-ть секцій')
    season = models.CharField(max_length=200, verbose_name = 'Сезон')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Coils(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    standart_size = models.CharField(max_length=10, verbose_name = 'Типорозмір')
    friction = models.CharField(max_length=50, verbose_name = 'Фрикціон')
    season = models.CharField(max_length=200, verbose_name = 'Сезон')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Cargo(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    material = models.CharField(max_length=100, verbose_name = 'Мітеріал')
    package_quantity = models.CharField(max_length=50, verbose_name = 'К-ть в упаковці(шт)')
    form = models.CharField(max_length=100, verbose_name = 'Форма')
    weight = models.CharField(max_length=9, verbose_name = 'Вага(г)')
    fastening = models.CharField(max_length=100, verbose_name = 'Кріплення')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Wobblers(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    weight = models.CharField(max_length=9, verbose_name = 'Вага(г)')
    fishing_technique = models.CharField(max_length=200, verbose_name = 'Техніка лову')
    buoyancy = models.CharField(max_length=200, verbose_name = 'Плавучисть')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Soft_baits(Product):
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    package_quantity = models.CharField(max_length=50, verbose_name = 'К-ть в упаковці(шт)')
    edible = models.BooleanField(default=True, verbose_name = 'Їстівна')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Spinners(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    weight = models.CharField(max_length=9, verbose_name = 'Вага(г)')
    package_quantity = models.CharField(max_length=50, verbose_name = 'К-ть в упаковці(шт)')
    features = models.CharField(max_length=200, verbose_name = 'Особливості')
    equipment = models.CharField(max_length=200, verbose_name = 'Оснащення')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Corbs_and_lines(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    length = models.CharField(max_length=50, verbose_name = 'Довжина(м)')
    diameter = models.CharField(max_length=50, verbose_name = 'Діаметер(мм)')
    tensile_load = models.CharField(max_length=50, verbose_name = 'Навантаження на розрив(кг)')
    purpose = models.CharField(max_length=200, verbose_name = 'Призначення')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Groundbaits_ozzles(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    spacialization = models.CharField(max_length=200, verbose_name = 'Спеціалізація')
    features = models.CharField(max_length=200, verbose_name = 'Особливості')
    size = models.CharField(max_length=3, verbose_name = 'Розмір(мм)')
    taste = models.CharField(max_length=200, verbose_name = 'Смак')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Feeders(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    package_quantity = models.CharField(max_length=50, verbose_name = 'К-ть в упаковці(шт)')
    weight = models.CharField(max_length=9, verbose_name = 'Вага(г)')
    material = models.CharField(max_length=100, verbose_name = 'Мітеріал')
    features = models.CharField(max_length=200, verbose_name = 'Особливості')
    form = models.CharField(max_length=100, verbose_name = 'Форма')
    season = models.CharField(max_length=200, verbose_name = 'Сезон')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Leashes(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    material = models.CharField(max_length=100, verbose_name = 'Мітеріал')
    package_quantity = models.CharField(max_length=50, verbose_name = 'К-ть в упаковці(шт)')
    assignmant = models.CharField(max_length=200, verbose_name = 'Призначення')
    tensile_load = models.CharField(max_length=50, verbose_name = 'Навантаження на розрив(кг)')
    length = models.CharField(max_length=50, verbose_name = 'Довжина(см)')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')


class Fishing_accessories(Product):
    brand = models.CharField(max_length=200, verbose_name = 'Бренд')
    type = models.CharField(max_length=200, verbose_name = 'Тип')
    assignmant = models.CharField(max_length=200, verbose_name = 'Призначення')
    season = models.CharField(max_length=200, verbose_name = 'Сезон')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_inf')
