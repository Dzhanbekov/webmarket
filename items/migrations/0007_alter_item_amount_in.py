# Generated by Django 4.0.4 on 2022-06-02 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_alter_item_size_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='amount_in',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='количество в линейке'),
        ),
    ]