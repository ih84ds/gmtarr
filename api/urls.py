from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth-token$', views.auth_token, name='auth_token'),
    url(r'^refresh-token$', refresh_jwt_token, name='refresh_token'),
    url(r'^event-registrants/(?P<event_id>[0-9]+)$', views.event_registrants, name='event_registrants'),

    # Flight Routes
    url(r'^flights$', views.FlightList.as_view(), name='flight_list'),
    url(r'^flights/(?P<pk>[0-9]+)$', views.FlightDetail.as_view(), name='flight_detail'),
    url(r'^flights/(?P<flight_id>[0-9]+)/players$', views.FlightPlayerList.as_view(), name='flight_player_list'),

    # Player Routes
    url(r'^players$', views.PlayerList.as_view(), name='player_list'),
    url(r'^players/(?P<pk>[0-9]+)$', views.PlayerDetail.as_view(), name='player_detail'),
]