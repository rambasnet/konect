# utility functions
import time


current_milliseconds = lambda: int(round(time.time()*1000))


def get_protocol(request):
    if request.is_secure():
        return 'https'
    else:
        return 'http'


def get_site_url(request):
    site_url = u'{0:s}://{1:s}'.format(get_protocol(request), request.get_host())
    return site_url


def user_media_path(request):
    path = u'img/{0}/{1}/'.format(request.user.id, current_milliseconds())
