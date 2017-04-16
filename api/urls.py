from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import refresh_jwt_token

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^docs/', include_docs_urls(title='Round Robin API Documentation')),

    # Token Routes
    url(r'^auth-token$', views.auth_token, name='auth_token'),
    url(r'^refresh-token$', refresh_jwt_token, name='refresh_token'),

    # User Info
    url(r'^userinfo$', views.userinfo, name='userinfo'),

    # League Routes
    url(r'^leagues$', views.LeagueListCreate.as_view(), name='league_list_create'),
    url(r'^leagues/mine$', views.LeagueListCreate.as_view(), {'mine': True}, name='league_list_create'),
    url(r'^leagues/(?P<pk>[0-9]+)$', views.LeagueRetrieveUpdateDestroy.as_view(), name='league_retrieve_update_destroy'),
    url(r'^leagues/(?P<league_id>[0-9]+)/flights$', views.LeagueFlightList.as_view(), name='league_flight_list'),
    url(r'^leagues/(?P<league_id>[0-9]+)/players$', views.LeaguePlayerList.as_view(), name='league_player_list'),

    # Flight Routes
    url(r'^flights$', views.FlightListCreate.as_view(), name='flight_list_create'),
    url(r'^flights/mine$', views.FlightListCreate.as_view(), {'mine': True}, name='flight_list_create'),
    url(r'^flights/(?P<pk>[0-9]+)$', views.FlightRetrieveUpdateDestroy.as_view(), name='flight_retrieve_update_destroy'),
    url(r'^flights/(?P<flight_id>[0-9]+)/players$', views.FlightPlayerList.as_view(), name='flight_player_list'),
    url(r'^flights/(?P<flight_id>[0-9]+)/matches$', views.FlightMatchList.as_view(), name='flight_match_list'),

    # Player Routes
    url(r'^players$', views.PlayerListCreate.as_view(), name='player_list_create'),
    url(r'^players/mine$', views.PlayerListCreate.as_view(), {'mine': True}, name='player_list_create'),
    url(r'^players/(?P<pk>[0-9]+)$', views.PlayerRetrieveUpdate.as_view(), name='player_retrieve_update'),
    url(r'^players/(?P<pk>[0-9]+)/delete$', views.PlayerDestroy.as_view(), name='player_destroy'),

    # Match Routes
    url(r'^matches/(?P<pk>[0-9]+)$', views.MatchRetrieve.as_view(), name='match_retrieve'),

    # WA Info Routes
    # url(r'^event-registrants/(?P<event_id>[0-9]+)$', views.event_registrants, name='event_registrants'),
]
