from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), 
    url(r'^use/$', views.use_system, name='use'), 
    url(r'^signin/$', views.user_signin, name='signin'), 
    url(r'^signup/$', views.user_signup, name='signup'), 
    url(r'^logout/$', views.user_logout, name='logout'), 
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
]
