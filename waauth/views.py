from django.shortcuts import render

# Python
import urllib, json
import logging

# Django
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

# Custom
from . import utils
from waauth.models import WAUser

logger = logging.getLogger(__name__)

def authenticate_view(request):
    code = request.GET.get('code')
    args = {
        'client_id': settings.WA_CLIENT_ID,
        'redirect_uri': request.build_absolute_uri(reverse('authenticate')),
        'scope': settings.WA_SCOPE,
    }
    
    if code != None:
        redirect_uri = request.GET.get('redirect_uri')
        user = authenticate(request=request, code=code, redirect_uri=redirect_uri)
        
        if user != None:
            login(request, user)
            return_uri = request.session.get('wa_return_uri')
            if return_uri is None:
                referer = request.META.get('HTTP_REFERER')
                if referer:
                    return HttpResponseRedirect(referer)
                else:
                    return HttpResponseRedirect('/')
            else:
                del request.session['wa_return_uri']
                return HttpResponseRedirect(return_uri)
        
        else:
            raise PermissionDenied
    else:
        request.session['wa_return_uri'] = request.GET.get('next')
        return HttpResponseRedirect('{}?{}'.format(settings.WA_OAUTH_LOGIN_URL, urllib.parse.urlencode(args)))

def register_view(request):
    return HttpResponseRedirect(settings.WA_JOIN_URL)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

def test_view(request):
    user = WAUser.objects.get(user=request.user)
    profile = utils.get_contact_info(user.access_token)
    return HttpResponse(json.dumps(profile))
    