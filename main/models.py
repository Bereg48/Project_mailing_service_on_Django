from django.db import models
from django.db.models import DateTimeField

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='email')
    name = models.CharField(max_length=250, verbose_name='ФИО')
    photo = models.ImageField(upload_to='main/', **NULLABLE, verbose_name='аватарка')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'{self.name} ({self.email}), ({self.comment})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    ONCE_DAY = 'once_a_day'
    ONCE_WEEK = 'once_a_week'
    ONCE_MONTH = 'once_a_month'
    FREQUENCY_OF_SENDING = [
        (ONCE_DAY, 'раз в день'),
        (ONCE_WEEK, 'раз в неделю'),
        (ONCE_MONTH, 'раз в месяц'),
    ]

    COMPLETED = 'completed'
    CREATED = 'created'
    LAUNCHED = 'launched'
    STATUS = [
        (COMPLETED, 'завершена'),
        (CREATED, 'создана'),
        (LAUNCHED, 'запущена'),
    ]

    frequency = models.CharField(max_length=15, choices=FREQUENCY_OF_SENDING, verbose_name='периодичность')
    time_mailing = DateTimeField(auto_now=False, auto_now_add=False, verbose_name='время рассылки')
    mailing_status = models.CharField(max_length=15, choices=STATUS, default=CREATED, verbose_name='статус рассылки')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='клиент сервиса')

    def __str__(self):
        return f'{self.frequency} ({self.mailing_status}), ({self.time_mailing})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    subject_letter = models.CharField(max_length=150, verbose_name='тема письма')
    body_letter = models.CharField(max_length=250, verbose_name='тело письма')
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f'{self.subject_letter} ({self.body_letter})'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingLogs(models.Model):
    datetime_of_last_try = models.DateTimeField(verbose_name='дата и время последней попытки')
    status_of_try = models.BooleanField(verbose_name='статус попытки')
    response_of_mail_server = models.BooleanField(verbose_name='ответ почтового сервера')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='клиент сервиса')
    mailing = models.OneToOneField('Mailing', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'{self.datetime_of_last_try} ({self.status_of_try}), ({self.response_of_mail_server})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

