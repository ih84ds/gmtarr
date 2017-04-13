from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth-token$', views.auth_token, name='auth_token'),
    url(r'^refresh-token$', refresh_jwt_token, name='refresh_token'),

    # League Routes
    url(r'^leagues$', views.LeagueListCreate.as_view(), name='league_list_create'),
    url(r'^leagues/(?P<pk>[0-9]+)$', views.LeagueRetrieveUpdateDestroy.as_view(), name='league_retrieve_update_destroy'),
    url(r'^leagues/(?P<league_id>[0-9]+)/flights$', views.LeagueFlightList.as_view(), name='league_flight_list'),
    url(r'^leagues/(?P<league_id>[0-9]+)/players$', views.LeaguePlayerList.as_view(), name='league_player_list'),

    # Flight Routes
    url(r'^flights$', views.FlightListCreate.as_view(), name='flight_list_create'),
    url(r'^flights/(?P<pk>[0-9]+)$', views.FlightRetrieveUpdateDestroy.as_view(), name='flight_retrieve_update_destroy'),
    url(r'^flights/(?P<flight_id>[0-9]+)/players$', views.FlightPlayerList.as_view(), name='flight_player_list'),

    # Player Routes
    url(r'^players$', views.PlayerListCreate.as_view(), name='player_list_create'),
    url(r'^players/(?P<pk>[0-9]+)$', views.PlayerRetrieveUpdate.as_view(), name='player_retrieve_update'),
    url(r'^players/(?P<pk>[0-9]+)/delete$', views.PlayerDestroy.as_view(), name='player_destroy'),

    # WA Info Routes
    url(r'^event-registrants/(?P<event_id>[0-9]+)$', views.event_registrants, name='event_registrants'),
]