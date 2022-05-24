from colorfield.fields import ColorField
from django.db import models


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
    old_price = models.PositiveIntegerField('старая Цена', default=0)
    new_price = models.PositiveIntegerField('новая Цена', default=0)
    description = models.TextField(verbose_name='О Товаре')
    size_range = models.CharField(max_length=20, verbose_name='размерный ряд')
    amount_in = models.PositiveIntegerField('количество в линейке', default=0)
    compound = models.CharField(max_length=200, verbose_name='Состав Ткани')
    material = models.CharField(max_length=200, verbose_name='Материал')
    is_in_cart = models.BooleanField(default=False)
    collection = models.ForeignKey(Collection, models.CASCADE, verbose_name='Коллекция')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemimage')
    image = models.ImageField(upload_to='item')

    class Meta:
        verbose_name = "фотографии товара"
        verbose_name_plural = "фотографии товара"


class ItemColor(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemcolor')
    custom_color = ColorField(default='#FF0000', verbose_name="Цвет")

    class Meta:
        verbose_name = "цвет товара"
        verbose_name_plural = "цвет товара"
