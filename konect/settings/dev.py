from konect.settings.base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'konect',
        'USER': 'konect',
        'PASSWORD': '4irtujkjnasdf9345!%$',
        'HOST': 'localhost'
    }
}

HTTP_PROTOCOL = 'http'

