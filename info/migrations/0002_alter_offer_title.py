# Generated by Django 4.0.4 on 2022-05-23 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='title',
            field=models.CharField(default='Публичная оферта', max_length=200, verbose_name='Заголовок'),
        ),
    ]