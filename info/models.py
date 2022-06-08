from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

CALL_TYPE = [('YES', 'ДА'), ('NO', 'НЕТ')]


class AboutUs(models.Model):
    """model for about us"""

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
    """model for news"""

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='news')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class HelpIcon(models.Model):
    """model for one icon to help"""

    icon = models.ImageField(upload_to='help')

    def __str__(self):
        return f'иконка'

    class Meta:
        verbose_name = 'Иконка для помощи'
        verbose_name_plural = 'Иконка для помощи'


class Help(models.Model):
    """model for help(question and answer)"""

    question = models.CharField(max_length=200, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    icon = models.ForeignKey(HelpIcon, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='helpicon')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Помощь'
        verbose_name_plural = 'Помощь'




class Offer(models.Model):
    """model for public offer"""

    title = models.CharField(max_length=200, verbose_name='Заголовок', default='Публичная оферта')
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публичная Оферта'
        verbose_name_plural = 'Публичная Оферта'


class Contacts(models.Model):
    """model for footer information"""

    header = models.ImageField(upload_to='header')
    footer = models.ImageField(upload_to='footer')
    email = models.EmailField(max_length=150, verbose_name='Электронная почта')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=False)
    phone_number_2 = PhoneNumberField(verbose_name='Номер телефона 2', unique=False)
    whatsapp_link = models.CharField(max_length=200, verbose_name='Ссылка на вотсап')
    telegram_link = models.CharField(max_length=200, verbose_name='Ссылка на телеграмм')
    instagram_link = models.CharField(max_length=200, verbose_name='Ссылка на инстаграмм')

    def __str__(self):
        return f'{self.phone_number}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if 'https://wa.me/' in self.whatsapp_link:
            pass
        else:
            self.whatsapp_link = 'https://wa.me/' + self.whatsapp_link

        if 'https://t.me/' in self.telegram_link:
            pass
        else:
            self.telegram_link = 'https://t.me/' + self.telegram_link

        if 'https://www.instagram.com/' in self.instagram_link:
            pass
        else:
            self.instagram_link = 'https://www.instagram.com/' + self.instagram_link

        super(Contacts, self).save()

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class Advantages(models.Model):
    """model for company's advantages"""

    icon = models.ImageField(upload_to='advantages', verbose_name='Иконка')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Наши Преимущества'
        verbose_name_plural = 'Наши Преимущества'


class MainPageIcon(models.Model):
    """model for main page slider"""

    icon = models.ImageField(upload_to='mainpage', verbose_name='Иконка')
    link = models.CharField(max_length=200, verbose_name='ссылка', blank=True, null=True)

    class Meta:
        verbose_name = 'Фото для главной страницы'
        verbose_name_plural = 'Фото для главной страницы'


class CallBack(models.Model):
    """model for callback"""

    name = models.CharField(max_length=200, verbose_name='имя')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=False)
    reason = models.CharField(max_length=200, verbose_name='тип обращения', default="обратный звонок")
    call_status = models.CharField(max_length=3, choices=CALL_TYPE, verbose_name='статус звонка', default='NO')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.reason} - {self.call_status}'

    class Meta:
        verbose_name = 'Обратный звонок'
        verbose_name_plural = 'Обратный звонок'


