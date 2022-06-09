from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

ORDER_STATUS = [('NEW', 'НОВЫЙ'), ('FRAMED', 'ОФОРМЛЕН'), ('CANCELED', 'ОТМЕНЕН')]


def validate_slash(value):
    one = value[0:2]
    two = value[3:]
    if str(one + two).isdecimal() and value[2] == '-'\
            and (int(one) + int(two)) % 2 == 0 \
            and int(one) <= int(two):
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
    date = models.DateField(verbose_name='дата добавления', auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.discount:
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

    def __str__(self):
        return f'{self.item} - {self.custom_color} - photo'


class Order(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    lastname = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(max_length=150, verbose_name='Электронная почта')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано", editable=False)
    country = models.CharField(max_length=150, verbose_name='Страна')
    city = models.CharField(max_length=150, verbose_name='Город')
    agreement = models.BooleanField(default=False, verbose_name='Согласие с условиями публичной оферты')
    order_status = models.CharField(
        max_length=12,
        choices=ORDER_STATUS,
        verbose_name='статус заказа',
        default='NEW',
        blank=True,
        null=True
    )
    item_quantity = models.IntegerField(verbose_name="Количество товаров", default=0)
    line_quantity = models.IntegerField(verbose_name="Количество линеек", default=0)
    price_before_discount = models.IntegerField(verbose_name="Общая цена без скидки", default=0)
    price_after_discount = models.IntegerField(verbose_name="Общая цена со скидкой", default=0)
    sum_of_discount = models.IntegerField(verbose_name="сумма скидки", default=0)

    def __str__(self):
        return f'{self.created_at.day}/' \
               f'{self.created_at.month}/' \
               f'{self.created_at.year} - ' \
               f'{self.name} - status {self.order_status}'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.item_quantity = ItemCart.get_total_quantity_of_item()
        self.line_quantity = ItemCart.get_total_quantity_of_item_line()
        self.price_before_discount = ItemCart.get_total_price_of_item_before_discount()
        self.price_after_discount = ItemCart.get_total_price_of_item_after_discount()
        self.sum_of_discount = self.price_before_discount - self.price_after_discount
        super(Order, self).save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    item = models.ForeignKey(Item, verbose_name="товар", on_delete=models.CASCADE, related_name='itemorder')
    title = models.CharField(verbose_name="описание", max_length=200)
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name='orderitem')
    image = models.ForeignKey(ItemImageColor, verbose_name="Фото", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.item} - {self.order}'

    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"


class ItemCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_item", verbose_name="Продукт",  blank=True, null=True)
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество линеек", blank=True, null=True)
    amount_item = models.PositiveIntegerField(default=0, verbose_name='количество товаров', blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='цена', default=0, blank=True, null=True)
    image = models.ForeignKey(ItemImageColor, on_delete=models.CASCADE, verbose_name='цвет', blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.item.discount:
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
        return f'{self.id} -- {self.item}: {self.amount_item} - {self.item.price * self.amount}'

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"



