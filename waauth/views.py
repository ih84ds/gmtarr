from django.shortcuts import render

# Python
import urllib, json

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

def authenticate_view(request):
    code = request.GET.get('code')
    args = {
        'client_id': settings.WA_CLIENT_ID,
        'redirect_uri': request.build_absolute_uri(reverse('authenticate')),
        'scope': settings.WA_SCOPE,
    }
    
    if code != None:
        user = authenticate(token=code, request=request)
        
        if user != None:
            login(request, user)
            return_uri = request.session.get('wa_return_uri')
            if return_uri is None:
                return HttpResponseRedirect('/')
            else:
                del request.session['wa_return_uri']
                return HttpResponseRedirect(return_uri)
        
        else:
            raise PermissionDenied
    else:
        if request.GET.get('ignorereferer') != '1':
            referer = request.META.get('HTTP_REFERER')
            if not referer is None:
                request.session['wa_return_uri'] = referer
        
        return HttpResponseRedirect('{}?{}'.format(settings.WA_OAUTH_LOGIN_URL, urllib.parse.urlencode(args)))

def register_view(request):
    return HttpResponseRedirect(settings.WA_JOIN_URL)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def test_view(request):
    user = WAUser.objects.get(user=request.user)
    profile = utils.get_contact_info(user.access_token, user.wa_id)
    return HttpResponse(json.dumps(profile))
    