from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Custom
from waauth import utils
from api.models import *
from api.serializers import *
from rest_framework import generics

@api_view(['GET'])
@permission_classes((AllowAny, ))
def index(request, *args, **kwargs):
    return Response({ 'msg': 'Hi. Welcome to the GMTA Round Robin API server.' })

@login_required()
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def auth_token(request, *args, **kwargs):
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

# Flight Views
class FlightList(generics.ListAPIView):
    """Gets list of all Flights."""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightDetail(generics.RetrieveAPIView):
    """Gets details for the specified Flight."""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

# Flight Views
class FlightPlayerList(generics.ListAPIView):
    """Gets list of all Players in the given flight."""

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
        q = Player.objects.filter(flights=flight)
        return q

    def get_serializer_class(self):
        user = self.request.user
        is_in_flight = self.get_flight_queryset().filter(players__users=user).count() > 0
        if is_in_flight or user.is_staff:
            return PlayerSerializer
        else:
            return PlayerPublicSerializer


# Player Views
class PlayerList(generics.ListAPIView):
    """Gets info for all players. Only admins can do this."""
    permission_classes = (IsAdminUser,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveUpdateAPIView):
    """Gets or Updates info for specified player."""
    serializer_class = PlayerSerializer

    def get_queryset(self):
        q = Player.objects.all()
        user = self.request.user
        # limit to self if not admin
        if not user.is_staff:
            q = q.filter(users=user)
        return q
