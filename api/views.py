from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.compat import is_authenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Custom
from waauth import utils
from api.models import *
from api.permissions import IsAdminUserOrReadOnly, IsAdminUserOrReadOnlyAuthenticated
from api.serializers import *
from rest_framework import generics

def index(request):
    return redirect('welcome')

@api_view(['GET'])
@permission_classes((AllowAny, ))
def welcome(request):
    return Response({ 'msg': 'Hi. Welcome to the GMTA Round Robin API server.' })

@api_view(['GET'])
@permission_classes((AllowAny, ))
def auth_token(request, *args, **kwargs):
    code = request.GET.get('code')
    redirect_uri = request.GET.get('redirect_uri')
    
    if code and redirect_uri:
        user = authenticate(request=request, code=code, redirect_uri=redirect_uri)
        if user != None:
            login(request, user)
        else:
            raise PermissionDenied
    else:
        raise Exception('code and redirect_uri parameters are required!')

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    data = {
        'token': token
    }
    return Response(data)

@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def event_registrants(request, event_id):
    # this is somewhat hacky as it requests a new token every time
    # FIXME: api auth token in session and refresh as necessary?
    token = utils.get_api_auth_token()
    access_token = token['access_token']
    events = utils.get_rr_events(access_token)
    first_event = events[0]
    event_id = first_event['Id']
    registrants = utils.get_rr_event_registrants(access_token, event_id)
    return Response(registrants)

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
    permission_classes = (AllowAny,)

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
        is_in_league = is_authenticated(user) and self.get_league_queryset().filter(players__user=user).exists()
        if is_in_league or user.is_staff:
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

# Match Views
class MatchRetrieve(generics.RetrieveAPIView):
    """Gets info for specified Match."""
    permission_classes = (AllowAny,)
    queryset = Match.objects.all()
    serializer_class = MatchPublicSerializer
