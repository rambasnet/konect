from django.shortcuts import render, redirect
from main import utility

from eprofile.models import Profile

# Create your views here.

def index(request):
    site_url = utility.get_site_url(request)
    if request.user.is_authenticated():
        #return redirect(reverse('profile:home'))
        user_profile = Profile.objects.get(user=request.user)
        site_url = utility.get_site_url(request)
        return render(request,
                  'eprofile/home.html',
                  dict(user_profile=user_profile, site_url=site_url,))
    else:
        return render(request,
                      'account/login_signup.html',
                      {
                          'site_url': site_url,
                      })


