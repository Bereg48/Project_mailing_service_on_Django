"""Обработка сигналов."""

from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone

from .models import Mailing
from .tasks import make_distribution

import logging
logger = logging.getLogger('trace')


@receiver(signals.post_save, sender=Mailing)
def create_distribution(sender, instance, created, **kwargs):
    """Создаем задачу на создание рассылки."""
    now = timezone.now()

    start_after = 1
    if instance.time_mailing > now:
        # Откладываем рассылку до времени старта
        start_after = int((instance.time_mailing - now).total_seconds())

    make_distribution.apply_async([instance.id,], countdown=start_after)
    logger.info(f'MAILING:{instance.id} created. Start over {start_after} sec.')