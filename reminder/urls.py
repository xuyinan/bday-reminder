from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), 
    url(r'^usesystem/$', views.use_system, name='usesystem'),

    url(r'^usesystem/birthday/$', views.birthday_email_send, name='birthday_email_send'),
    url(r'^usesystem/birthday/done/$', views.birthday_email_done, name='birthday_email_done'),

    url(r'^usesystem/custom/$', views.custom_email, name='custom_email'), 
    url(r'^usesystem/custom/message/$', views.custom_email_send, name='custom_email_send'), 
    url(r'^usesystem/custom/message/done/$', views.custom_email_done, name='custom_email_done'), 

    url(r'^signin/$', views.user_signin, name='signin'), 
    url(r'^signup/$', views.user_signup, name='signup'), 
    url(r'^logout/$', views.user_logout, name='logout'), 
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/thanks/$', views.contact_thanks, name='contact_thanks'),
]
