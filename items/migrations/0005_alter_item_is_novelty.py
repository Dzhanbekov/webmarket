# Generated by Django 4.0.4 on 2022-05-31 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_rename_bestseller_item_is_bestseller_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='is_novelty',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
