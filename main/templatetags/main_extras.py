import datetime

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def current_year():
    return datetime.date.today().year


@register.simple_tag
def brand_name():
    return settings.BRAND_NAME


@register.filter
def month_name(int_mth):
    if int_mth == 1:
        return 'January'
    elif int_mth == 2:
        return 'February'
    elif int_mth == 3:
        return 'March'
    elif int_mth == 4:
        return 'April'
    elif int_mth == 5:
        return 'May'
    elif int_mth == 6:
        return 'June'
    elif int_mth == 7:
        return 'July'
    elif int_mth == 8:
        return 'August'
    elif int_mth == 9:
        return 'September'
    elif int_mth == 10:
        return 'October'
    elif int_mth == 11:
        return 'November'
    elif int_mth == 12:
        return 'December'
    else:
        return ''
