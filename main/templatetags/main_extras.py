import datetime

from django import template
from django.conf import settings

from main import utility

register = template.Library()


@register.simple_tag
def current_year():
    return datetime.date.today().year


@register.simple_tag
def brand_name():
    return settings.BRAND_NAME

