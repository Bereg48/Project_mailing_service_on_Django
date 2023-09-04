from django import template

from main.models import Client

register = template.Library()


@register.filter()
def mediapath(value):
    if value:
        return f'/media/{value}'

    return '#'


@register.simple_tag()
def all_version():
    return Client.objects.all()
