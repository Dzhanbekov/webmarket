from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


def validate_slash(value):
    if str(value[0:2] + value[3:]).isdecimal() and value[2] == '-' \
            and int(value[0:2]) + int(value[3:]) % 2 == 0 and int(value[0:2]) < int(value[3:]):
        return value
    else:
        raise ValidationError("this field must be, for example 44-50")


class Collection(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование коллекции')
    image = models.ImageField(upload_to='collection', verbose_name='Картинка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='Описание товара')
    item_id = models.CharField(max_length=200, unique=True, verbose_name='Артикул', blank=True, null=True)
    basic_price = models.PositiveIntegerField('Основная Цена', default=0)
    price = models.PositiveIntegerField('новая Цена', default=0, blank=True, null=True)
    discount = models.PositiveIntegerField(default=0, verbose_name='процент скидки', blank=True, null=True)
    description = models.TextField(verbose_name='О Товаре')
    size_range = models.CharField(max_length=5, verbose_name='размерный ряд', validators=[validate_slash])
    amount_in = models.PositiveIntegerField('количество в линейке', default=0, blank=True)
    compound = models.CharField(max_length=200, verbose_name='Состав Ткани')
    material = models.CharField(max_length=200, verbose_name='Материал')
    is_in_cart = models.BooleanField(default=False, blank=True, null=True)
    is_in_favourite = models.BooleanField(default=False, verbose_name='избранное?', blank=True, null=True)
    is_novelty = models.BooleanField(default=False, blank=True, null=True, verbose_name='новинка?')
    is_bestseller = models.BooleanField(default=False, blank=True, null=True, verbose_name='хит продаж?')
    collection = models.ForeignKey(Collection, models.CASCADE, verbose_name='Коллекция', related_name='itemcollection')
    date = models.DateField(verbose_name='дата добавления',  blank=True, null=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        percent = self.basic_price * self.discount / 100
        self.price = self.basic_price - percent
        self.amount_in = (int(self.size_range[3:]) - int(self.size_range[0:2]) + 2) // 2
        super(Item, self).save()
        super(Item, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ItemImageColor(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemimage')
    image = models.ImageField(upload_to='item')
    custom_color = ColorField(default='#FF0000', verbose_name="Цвет")

    class Meta:
        verbose_name = "фотографии товара"
        verbose_name_plural = "фотографии товара"


class Order(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    lastname = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(max_length=150, verbose_name='Электронная почта')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано", editable=False)
    country = models.CharField(max_length=150, verbose_name='Страна')
    city = models.CharField(max_length=150, verbose_name='Город')
    agreement = models.BooleanField(default=False, verbose_name='Согласие с условиями публичной оферты')

    def __str__(self):
        return f'{self.created_at.year}/' \
               f'{self.created_at.month}/' \
               f'{self.created_at.day} ' \
               f'{self.created_at.hour}:{self.created_at.minute} - '\
               f'{self.name}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class ItemCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_item", verbose_name="Продукт")
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество линеек", blank=True, null=True)
    amount_item = models.PositiveIntegerField(default=0, verbose_name='количество товаров', blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item", verbose_name="Заказ")
    price = models.PositiveIntegerField(verbose_name='цена', default=0, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.item.discount is not None:
            self.price = self.item.price * self.amount
        else:
            self.price = self.item.basic_price * self.amount
        self.amount_item = self.amount * self.item.amount_in
        super(ItemCart, self).save()

    @staticmethod
    def get_total_price_of_item_before_discount():
        total = 0
        for orderitem in ItemCart.objects.all():
            total += orderitem.item.basic_price * orderitem.amount
        return total

    @staticmethod
    def get_total_price_of_item_after_discount():
        total = 0
        for orderitem in ItemCart.objects.all():
            total += orderitem.item.price * orderitem.amount
        return total

    @staticmethod
    def get_total_quantity_of_item():
        total = 0
        for orderitem in ItemCart.objects.all():
            total += orderitem.amount_item
        return total

    @staticmethod
    def get_total_quantity_of_item_line():
        total = 0
        for orderitem in ItemCart.objects.all():
            total += orderitem.amount
        return total

    def __str__(self):
        return f'{self.item}:{self.amount_item} - {self.item.price * self.amount}'

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class SearchHelper(models.Model):
    name = models.CharField(max_length=250)
    counter = models.IntegerField()

    def __str__(self):
        return self.name




