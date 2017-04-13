from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth-token$', views.auth_token, name='auth_token'),
    url(r'^refresh-token$', refresh_jwt_token, name='refresh_token'),

    # League Routes
    url(r'^leagues$', views.LeagueList.as_view(), name='league_list'),
    url(r'^leagues/(?P<pk>[0-9]+)$', views.LeagueDetail.as_view(), name='league_detail'),
    url(r'^leagues/(?P<league_id>[0-9]+)/flights$', views.LeagueFlightList.as_view(), name='league_flight_list'),
    url(r'^leagues/(?P<league_id>[0-9]+)/players$', views.LeaguePlayerList.as_view(), name='league_player_list'),

    # Flight Routes
    url(r'^flights$', views.FlightList.as_view(), name='flight_list'),
    url(r'^flights/create$', views.FlightCreate.as_view(), name='flight_create'),
    url(r'^flights/(?P<pk>[0-9]+)$', views.FlightDetail.as_view(), name='flight_detail'),
    url(r'^flights/(?P<flight_id>[0-9]+)/players$', views.FlightPlayerList.as_view(), name='flight_player_list'),

    # Player Routes
    url(r'^players$', views.PlayerList.as_view(), name='player_list'),
    url(r'^players/(?P<pk>[0-9]+)$', views.PlayerDetail.as_view(), name='player_detail'),

    # WA Info Routes
    url(r'^event-registrants/(?P<event_id>[0-9]+)$', views.event_registrants, name='event_registrants'),
]