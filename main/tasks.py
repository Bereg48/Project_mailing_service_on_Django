# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
#
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")
#
#
# @register_job(scheduler, "interval", seconds=5)
# def test_job():
#     print("Test job executed")
#
#
# register_events(scheduler)
# scheduler.start()


"""Задачи запускаемые в асинхронном режиме."""

import datetime

from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail

from django.conf import settings
from config.celery import app
from .models import Message, Client, Mailing, MailingLogs

import logging

logger = logging.getLogger('trace')


@shared_task()
def send_one_notify(mailing_id: int, client_id: int):
    """Отправка одного сообщения."""
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)

    # Создаем сообщение в базе
    now = timezone.now()
    message = Message(created=now, client=client, mailing=mailing, )
    message.save()

    now = datetime.datetime.now()
    for ms in Mailing.objects.filter(status=Mailing.STATUS):
        for mc in ms.client_set.all():
            ml = MailingLogs.objects.filter(client=mc.client, settings=ms)
            if ml.exists():
                last_try_date = ml.order_by('last').first()
                if ms.frequency == Mailing.ONCE_DAY:
                    if (now - last_try_date).days >= 1:
                        send_mail(ms, mc)
                elif ms.frequency == Mailing.ONCE_WEEK:
                    if (now - last_try_date).days >= 7:
                        send_mail(ms, mc)
                elif ms.frequency == Mailing.ONCE_MONTH:
                    if (now - last_try_date).days >= 30:
                        send_mail(ms, mc)
            else:
                send_mail(ms, mc)
            pass


def recipients(mailing_id: int):
    """Выбираем получателей рассылки по фильтру."""
    dist = Mailing.objects.get(pk=mailing_id)

    q = Q()
    if dist.filter_code:
        q = q & Q(code=dist.filter_code)
    if dist.filter_tag:
        q = q & Q(tag=dist.filter_tag)
    return Client.objects.filter(q)


@shared_task()
def make_distribution(mailing_id: int):
    """Создаем задачи на отправку сообщений."""
    clients = recipients(mailing_id)

    for client in clients:
        send_one_notify.delay(mailing_id, client.pk)


@shared_task()
def send_daily_stats():
    """Отправляем статистику за вчера."""
    yesterday = timezone.now() - datetime.timedelta(days=1)
    dist_count = Mailing.objects.filter(
        time_mailing__year=yesterday.year,
        time_mailing__month=yesterday.month,
        time_mailing__day=yesterday.day
    )
    mess_count = Message.objects.filter(
        created__year=yesterday.year,
        created__month=yesterday.month,
        created__day=yesterday.day
    )

    # Отправляем письмо
    return send_mail(
        f'Daily Stats {yesterday.date()}',
        f'Distributions: {dist_count} Messages: {mess_count}',
        settings.SERVER_EMAIL,
        [settings.SERVER_EMAIL, ],
        fail_silently=False,
    )
