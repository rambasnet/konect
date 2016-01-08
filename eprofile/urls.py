from django.conf.urls import url

from eprofile import views

app_name = 'profile'

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
    url(r'^update_cover_photo/$', views.update_cover_photo, name='update_cover_photo'),
    url(r'^update_profile_photo/$', views.update_profile_photo, name='update_profile_photo'),
    url(r'^update_card/$', views.update_card, name='update_card'),
    url(r'^update_summary/$', views.update_summary, name='update_summary')
]
