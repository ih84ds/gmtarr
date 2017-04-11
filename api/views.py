from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Custom
from waauth import utils

@login_required(redirect_field_name="redirect_uri")
def index(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

@login_required(redirect_field_name="redirect_uri")
@api_view(['GET'])
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