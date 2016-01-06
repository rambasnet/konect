from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def profile(request):
    return render(request,
                  'eprofile/profile.html',
                  dict(user=request.user))


@login_required
def edit_profile(request):
    pass


@login_required
def update_cover_photo(request):
    pass


@login_required
def update_profile_photo(request):
    pass
