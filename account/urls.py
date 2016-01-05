from django.conf.urls import url

from account import views

app_name = 'account'

urlpatterns = [
    url(r'^recover/', views.recover, name='recover'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^reset_password/(?P<key>.*)/$', views.reset_password, name='reset_password_key'),
]