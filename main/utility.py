# utility functions


def get_protocol(request):
    if request.is_secure():
        return 'https'
    else:
        return 'http'


def get_site_url(request):
    site_url = u'{0:s}://{1:s}'.format(get_protocol(request), request.get_host())
    return site_url
