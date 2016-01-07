from django.shortcuts import render, redirect
from main import utility

from django.core.urlresolvers import reverse


# Create your views here.

def index(request):
    site_url = utility.get_site_url(request)
    if request.user.is_authenticated():
        return redirect(reverse('profile:profile'))
    else:
        return render(request,
                      'account/login_signup.html',
                      {
                          'site_url': site_url,
                      })


