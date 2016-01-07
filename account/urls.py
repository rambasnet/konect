from django.conf.urls import url

from account import views

app_name = 'account'

urlpatterns = [
    url(r'^recover/', views.recover, name='recover'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^reset_password/(?P<key>.*)/$', views.reset_password, name='reset_password_key'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^activate/(.*)/$', views.activate, name='activate'),
    url(r'^activation$', views.activation, name='activation'),
]