# Generated by Django 4.0.4 on 2022-05-30 11:36

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование коллекции')),
                ('image', models.ImageField(upload_to='collection', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Коллекция',
                'verbose_name_plural': 'Коллекции',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Описание товара')),
                ('item_id', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Артикул')),
                ('basic_price', models.PositiveIntegerField(default=0, verbose_name='Основная Цена')),
                ('price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='новая Цена')),
                ('discount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='процент скидки')),
                ('description', models.TextField(verbose_name='О Товаре')),
                ('size_range', models.CharField(max_length=20, verbose_name='размерный ряд')),
                ('amount_in', models.PositiveIntegerField(default=0, verbose_name='количество в линейке')),
                ('compound', models.CharField(max_length=200, verbose_name='Состав Ткани')),
                ('material', models.CharField(max_length=200, verbose_name='Материал')),
                ('is_in_cart', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, null=True, verbose_name='дата добавления')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemcollection', to='items.collection', verbose_name='Коллекция')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('lastname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=150, verbose_name='Электронная почта')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('country', models.CharField(max_length=150, verbose_name='Страна')),
                ('city', models.CharField(max_length=150, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ItemImageColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='item')),
                ('custom_color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None, verbose_name='Цвет')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemimage', to='items.item')),
            ],
            options={
                'verbose_name': 'фотографии товара',
                'verbose_name_plural': 'фотографии товара',
            },
        ),
        migrations.CreateModel(
            name='ItemCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Количество')),
                ('price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='цена')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='items.item', verbose_name='Продукт')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='items.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('device', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
