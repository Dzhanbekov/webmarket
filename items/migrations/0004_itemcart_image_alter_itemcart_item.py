# Generated by Django 4.0.4 on 2022-06-07 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_remove_itemcart_image_alter_itemcart_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcart',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.itemimagecolor', verbose_name='цвет'),
        ),
        migrations.AlterField(
            model_name='itemcart',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='items.item', verbose_name='Продукт'),
        ),
    ]
