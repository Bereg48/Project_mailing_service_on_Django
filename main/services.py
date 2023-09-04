from django.conf import settings
from django.core.cache import cache

from main.models import Client


def get_cached_subject_for_category():
    if settings.CACHES_ENABLED:
        subject_list = cache.get('subject_list')
        if subject_list is None:
            subject_list = Client.objects.all()
            cache.set('subject_list', subject_list)
    else:
        subject_list = Client.objects.all()
        return subject_list