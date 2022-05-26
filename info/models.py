from django.db import models


class AboutUs(models.Model):
    description = models.TextField(verbose_name='О нас')
    image_1 = models.ImageField(upload_to='about')
    image_2 = models.ImageField(upload_to='about')
    image_3 = models.ImageField(upload_to='about')

    def __str__(self):
        return self.description[:20]

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'


class News(models.Model):

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='news')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class Help(models.Model):
    question = models.CharField(max_length=200, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Помощь'
        verbose_name_plural = 'Помощь'


class Offer(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок', default='Публичная оферта')
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публичная Оферта'
        verbose_name_plural = 'Публичная Оферта'


class Contacts(models.Model):
    email_tech = models.CharField(max_length=200, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=200, verbose_name='Телефонный номер')
    phone_number_2 = models.CharField(max_length=200, verbose_name='Телефонный номер 2')
    whatsapp_link = models.CharField(max_length=200, verbose_name='Ссылка на вотсап')
    telegram_link = models.CharField(max_length=200, verbose_name='Ссылка на вотсап')
    instagram_link = models.CharField(max_length=200, verbose_name='Ссылка на вотсап')

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class Advantages(models.Model):
    icon = models.ImageField(upload_to='advantages', verbose_name='Иконка')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Наши Преимущества'
        verbose_name_plural = 'Наши Преимущества'


class MainPageIcon(models.Model):
    icon = models.ImageField(upload_to='mainpage', verbose_name='Иконка')
    link = models.CharField(max_length=200, verbose_name='ссылка', blank=True, null=True)

    class Meta:
        verbose_name = 'Фото для главной страницы'
        verbose_name_plural = 'Фото для главной страницы'
