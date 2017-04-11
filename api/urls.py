from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth-token$', views.auth_token, name='auth_token'),
    url(r'^$', views.index, name='index'),
]