from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

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