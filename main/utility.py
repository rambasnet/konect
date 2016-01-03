# utility functions


def get_protocol(request):
    if request.is_secure():
        return 'https'
    else:
        return 'http'

