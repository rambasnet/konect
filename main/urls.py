from django.conf.urls import url

from main import views
from eprofile import views as pView

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', pView.home, name='home'),
    url(r'^index/$', pView.home, name='default'),
]