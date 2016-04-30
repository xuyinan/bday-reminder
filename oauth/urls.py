from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^drchrono/login/$', views.drchrono_login, name='drchrono_login'),
    url(r'^drchrono/login/done/$', views.drchrono_auth, name='drchrono_login_done'), 
]

