from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from eprofile.models import Photo, Profile
from eprofile.forms import ImageUploadForm, ProfileCardForm
from main import utility
# Create your views here.


@login_required
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    site_url = utility.get_site_url(request)
    return render(request,
                  'eprofile/profile.html',
                  dict(user_profile=user_profile, site_url= site_url,))


@login_required
def edit_profile(request):
    profile = Profile(user=request.user)
    return HttpResponse('hello there!')


@login_required
def update_cover_photo(request):
    # Handle file upload
    site_url = utility.get_site_url(request)
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cover = Photo(user=request.user, photo=request.FILES['img_file'])
            cover.save()
            # print('name=', cover.photo.name)
            # print('path=', cover.photo.path)
            # print('url=', cover.photo.url)
            # Redirect to the document list after POST
            profile = Profile.objects.get(user=cover.user)
            profile.cover_photo = cover.photo.name
            profile.save(update_fields=['cover_photo'])
            return HttpResponseRedirect(reverse('profile:profile'))
    else:
        form = ImageUploadForm()  # A empty, unbound form

    message = ''
    return render(request,
        'eprofile/photos.html',
        dict(site_url=site_url,
             form_heading='Upload Cover Photo',
             instruction='Cover photo must be at least 300px tall and 900px wide.',
             action=reverse('profile:update_cover_photo'),
             form=form,
             user_profile=user_profile))


@login_required
def update_profile_photo(request):
    site_url = utility.get_site_url(request)
    user_profile = Profile.objects.get(user=request.user)
    # Handle file upload
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(user=request.user, photo=request.FILES['img_file'])
            photo.save()
            # print('name=', cover.photo.name)
            # print('path=', cover.photo.path)
            # print('url=', cover.photo.url)
            # Redirect to the document list after POST
            profile = Profile.objects.get(user=photo.user)
            profile.profile_photo = photo.photo.name
            profile.save(update_fields=['profile_photo'])
            return HttpResponseRedirect(reverse('profile:profile'))
    else:
        form = ImageUploadForm()  # A empty, unbound form

    return render(request,
        'eprofile/photos.html',
        dict(site_url=site_url,
             form_heading='Upload Profile Photo',
             instruction='Cover photo must be at least 200px tall and 200px wide.',
             action=reverse('profile:update_profile_photo'),
             form=form,
             user_profile=user_profile))


@login_required
def update_card(request):
    site_url = utility.get_site_url(request)
    user_profile = Profile.objects.get(user=request.user)
    # load existing card info
    pro = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        card_form = ProfileCardForm(request.POST, instance=pro)
        if card_form.is_valid():
            card_form.save()
            return HttpResponseRedirect(reverse('profile:profile'))
        else:
            print('errors = ', card_form.errors)
    else:
        card_form = ProfileCardForm(instance=pro)

    return render(request,
                  'eprofile/update_card.html',
                  dict(site_url=site_url,
                       form=card_form,
                       user_profile=user_profile))
