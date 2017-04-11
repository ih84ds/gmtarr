from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth-token$', views.auth_token, name='auth_token'),
    url(r'^event-registrants/(?P<event_id>[0-9]+)$', views.event_registrants, name='event_registrants'),
    url(r'^$', views.index, name='index'),
]