from operator import itemgetter

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db.models import Q

from rest_framework_jwt.settings import api_settings
from rest_framework import generics, status, views
from rest_framework.compat import is_authenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Custom
from waauth import utils as wautils
from api.models import *
from api.permissions import IsAdminUserOrReadOnly, IsAdminUserOrReadOnlyAuthenticated, IsAdminUserOrMatchPlayerOrReadOnly
from api.serializers import *

def index(request):
    return redirect('welcome')

@api_view(['GET'])
@permission_classes((AllowAny, ))
def welcome(request):
    return Response({ 'msg': 'Hi. Welcome to the GMTA Round Robin API server.' })

@api_view(['GET'])
@permission_classes((AllowAny, ))
def auth_token(request, *args, **kwargs):
    """Authenticates a user using an access code retrieved from WA OAuth Login.

    #### Required Query Parameters

    * code: the code retruned from WA OAuth Login page after redirecting back to the client.
    * reirect_uri: the redirect_uri parameter that was passed to WA login when the code was retrieved.
    """
    code = request.GET.get('code')
    redirect_uri = request.GET.get('redirect_uri')
    
    if code and redirect_uri:
        user = authenticate(request=request, code=code, redirect_uri=redirect_uri)
        if not user:
            raise PermissionDenied
    else:
        raise AuthenticationFailed('code and redirect_uri parameters are required!')

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    data = {
        'token': token
    }
    return Response(data)

@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def event_info(request, event_id):
    # this is somewhat hacky as it requests a new token every time
    # FIXME: api auth token in session and refresh as necessary?
    token = wautils.get_api_auth_token()
    access_token = token['access_token']
    event = wautils.get_rr_event_info(access_token, event_id)
    return Response(event)

@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def event_create_league(request, event_id):
    # this is somewhat hacky as it requests a new token every time
    # FIXME: api auth token in session and refresh as necessary?
    token = wautils.get_api_auth_token()
    access_token = token['access_token']
    league = utils.create_league_for_event(access_token, event_id)
    players = utils.import_players_for_event(access_token, league, event_id)
    return redirect('league_retrieve_update_destroy', pk=league.id)

@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def event_registrants(request, event_id):
    # this is somewhat hacky as it requests a new token every time
    # FIXME: api auth token in session and refresh as necessary?
    token = wautils.get_api_auth_token()
    access_token = token['access_token']
    registrants = wautils.get_rr_event_registrants(access_token, event_id)
    return Response(registrants)

@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def events(request):
    # this is somewhat hacky as it requests a new token every time
    # FIXME: api auth token in session and refresh as necessary?
    token = wautils.get_api_auth_token()
    access_token = token['access_token']
    events = wautils.get_rr_events(access_token)
    return Response(events)

@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def flight_generate_schedule(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise NotFound()
    utils.generate_matches_for_flight(flight)
    return redirect('flight_match_list', flight_id=flight_id)

# User Info Views
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def userinfo(request):
    user = request.user
    data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'last_login': user.last_login,
        'wa_contact_id': user.wa_user and user.wa_user.wa_id
    }
    return Response(data)

# League Views
class LeagueListCreate(generics.ListCreateAPIView):
    """Gets list of all Leagues.
    """
    serializer_class = LeagueSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        q = League.objects.all()
        mine = self.kwargs.get('mine')
        user = self.request.user
        if mine:
            if is_authenticated(user):
                q = q.filter(players__user=user)
            else:
                # anonymous users don't have any.
                q = q.none()
        return q

class LeagueRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Gets details for the specified League."""
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

class LeagueFlightList(generics.ListAPIView):
    """Gets list of all Flights in the given League."""
    serializer_class = FlightSerializer
    permission_classes = (AllowAny,)

    def get_league(self):
        try:
            league = self.get_league_queryset().get()
        except:
            league = None
        return league

    def get_league_queryset(self):
        return League.objects.filter(pk=self.kwargs['league_id'])

    def get_queryset(self):
        league = self.get_league()
        if not league:
            return None
        q = Flight.objects.filter(league=league)
        return q

class LeaguePlayerList(generics.ListAPIView):
    """Gets list of all Players in the given League."""
    permission_classes = (AllowAny,)

    def get_league(self):
        try:
            league = self.get_league_queryset().get()
        except:
            league = None
        return league

    def get_league_queryset(self):
        return League.objects.filter(pk=self.kwargs['league_id'])

    def get_queryset(self):
        league = self.get_league()
        if not league:
            return None
        q = Player.objects.filter(league=league)
        return q

    def get_serializer_class(self):
        user = self.request.user
        # is_in_league = is_authenticated(user) and self.get_league_queryset().filter(players__user=user).exists()
        if user.is_staff:
            # include contact info
            return PlayerSerializer
        else:
            return PlayerPublicSerializer

# Flight Views
class FlightListCreate(generics.ListCreateAPIView):
    """Gets list of all Flights."""
    serializer_class = FlightSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        q = Flight.objects.all()
        mine = self.kwargs.get('mine')
        user = self.request.user
        if mine:
            if is_authenticated(user):
                q = q.filter(players__user=user)
            else:
                # anonymous users don't have any.
                q = q.none()
        return q

class FlightRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Gets details for the specified Flight."""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

class FlightPlayerList(generics.ListAPIView):
    """Gets list of all Players in the given Flight."""
    permission_classes = (AllowAny,)

    def get_flight(self):
        try:
            flight = self.get_flight_queryset().get()
        except:
            flight = None
        return flight

    def get_flight_queryset(self):
        return Flight.objects.filter(pk=self.kwargs['flight_id'])

    def get_queryset(self):
        flight = self.get_flight()
        if not flight:
            return None
        q = Player.objects.filter(flight=flight)
        return q

    def get_serializer_class(self):
        user = self.request.user
        is_in_flight = is_authenticated(user) and self.get_flight_queryset().filter(players__user=user).exists()
        if is_in_flight or user.is_staff:
            # include contact info
            return PlayerSerializer
        else:
            return PlayerPublicSerializer

class FlightMatchList(generics.ListAPIView):
    """Gets list of all Matches in the given Flight."""
    permission_classes = (AllowAny,)
    serializer_class = MatchPublicSerializer

    def get_flight(self):
        try:
            flight = self.get_flight_queryset().get()
        except:
            flight = None
        return flight

    def get_flight_queryset(self):
        return Flight.objects.filter(pk=self.kwargs['flight_id'])

    def get_queryset(self):
        flight = self.get_flight()
        if not flight:
            return None
        q = Match.objects.filter(flight=flight)
        return q

@api_view(['GET'])
@permission_classes((AllowAny, ))
def flight_standings(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise NotFound()
    data = []
    for p in flight.players.all():
        match_record = p.get_record()
        games_record = p.get_games_record()
        data.append({
            'player_id': p.id,
            'name': p.name,
            'wins': match_record[0],
            'losses': match_record[1],
            'ties': match_record[2] or 0,
            'game_wins': games_record[0],
            'game_losses': games_record[1],
        })
    data = sorted(data, key=itemgetter('wins', 'game_wins'), reverse=True)
    return Response(data)

# Player Views
class PlayerListCreate(generics.ListCreateAPIView):
    """Gets info for all accessible players.

    If user is an admin and not requesting "mine", returns all players.
    If user is non-admin or is requesting "mine", returns all players that belong to the current user.
    """
    permission_classes = (IsAdminUserOrReadOnlyAuthenticated,)
    serializer_class = PlayerSerializer
    filter_fields = ('id', 'user')

    def get_queryset(self):
        q = Player.objects.all()
        mine = self.kwargs.get('mine')
        user = self.request.user
        if mine:
            if is_authenticated(user):
                q = q.filter(user=user)
            else:
                # anonymous users don't have any.
                q = q.none()
        elif not user.is_staff:
            # non-admin can only list their own players
            q = q.filter(user=user)
        return q

class PlayerRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """Gets or Updates info for specified Player.

    If user is non-admin, only that user's players can be updated
    """
    serializer_class = PlayerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        q = Player.objects.all()
        user = self.request.user
        # limit to self if not admin
        if not user.is_staff:
            q = q.filter(user=user)
        return q

class PlayerDestroy(generics.DestroyAPIView):
    """Deletes a player.

    Only admins can do this.
    """
    permission_classes = (IsAdminUser,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class MatchRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """Gets or Updates info for specified Match.

    If user is non-admin, only that user's matches can be updated
    """
    queryset = Match.objects.all()
    serializer_class = MatchPlayerSerializer
    permission_classes = (IsAdminUserOrMatchPlayerOrReadOnly,)

    def get_serializer_class(self):
        # user = self.request.user
        # is_match_player = is_authenticated(user) and self.get_queryset().filter(Q(home_player__user=user) | Q(visitor_player__user=user)).exists()
        # TODO: add Match Admin Serializer so admins can edit more stuff
        return MatchPlayerSerializer
