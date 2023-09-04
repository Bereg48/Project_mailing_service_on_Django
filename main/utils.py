from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMessage

from config.settings import EMAIL_HOST_USER
from main.models import MailingLogs, Mailing
from django.core.mail import send_mail

# send_mail(
#     "Subject here",
#     "Here is the message.",
#     "from@example.com",
#     ["to@example.com"],
#     fail_silently=False,
# )

# def send_mails():
#     now = datetime.datetime.now()
#     for ms in Mailing.objects.filter(status=Mailing.STATUS):
#         for mc in ms.client_set.all():
#             ml = MailingLogs.objects.filter(client=mc.client, settings=ms)
#             if ml.exists():
#                 last_try_date = ml.order_by('-last_try').first()
#                 if ms.frequency == Mailing.ONCE_DAY:
#                     if (now - last_try_date).days >= 1:
#                         send_mail(ms, mc)
#                 elif ms.frequency == Mailing.ONCE_WEEK:
#                     if (now - last_try_date).days >= 7:
#                         send_mail(ms, mc)
#                 elif ms.frequency == Mailing.ONCE_MONTH:
#                     if (now - last_try_date).days >= 30:
#                         send_mail(ms, mc)
#             else:
#                 send_mail(ms, mc)
#
#
# def send_mail_for_verify(request, user):
#     current_site = get_current_site(request)
#     context = {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': token_generator.make_token(user),
#     }
#     massage = render_to_string(
#         'users/verify_email.html',
#         context=context,
#     )
#     email = EmailMessage(
#         'Veryfi email',
#         massage,
#         to=[user.email],
#     )
#     email.send()


import datetime
from celery import Celery
from main.models import Mailing

app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Setup and call send_reminders() every 60 seconds.

    sender.add_periodic_task(60.0, send_reminders, name='check reminders to be sent every minute')


@app.task
def send_reminders():
    # Celery task that gets all groups that needs reminders to be sent 30 minutes from now

    thirty_minutes_from_now = datetime.datetime.now() + datetime.timedelta(minutes=30)

    mailing = Mailing.objects.filter(
        time_mailing__hour=thirty_minutes_from_now.hour,
        time_mailing__minute=thirty_minutes_from_now.minute
    ).prefetch_related("client")

    for mailin in mailing:
        for member in mailin.client.all():
            send_email_task.delay(member.email)


@app.task
def send_email_task(recipient):
    # Celery task to send emails

    send_mail(
        "Subject here",
        "Here is the message.",
        EMAIL_HOST_USER,
        [recipient],
        fail_silently=False,
    )
