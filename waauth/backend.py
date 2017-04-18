# Python
import requests, base64

# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

# Custom
from waauth.models import WAUser
import waauth.utils as utils

class WAAuthBackend(ModelBackend):
    def authenticate(self, request=None, code=None, redirect_uri=None):
        """Authenticates a user using an access code retrieved from WA OAuth Login.

        Keyword arguments:
        request -- the current http request object
        code -- the code retruned from WA OAuth Login page after redirecting back to the client
        reirect_uri -- the redirect_uri parameter that was passed to WA login when the code was retrieved
        """
        if not redirect_uri:
            redirect_uri = request.build_absolute_uri(reverse('authenticate'))
        args = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': settings.WA_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'scope': settings.WA_SCOPE,
        }

        access_header_raw = '{}:{}'.format(settings.WA_CLIENT_ID, settings.WA_CLIENT_SECRET)
        authorization_header = base64.b64encode(access_header_raw.encode()).decode()
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'Basic {}'.format(authorization_header)
        }

        r = requests.post(settings.WA_TOKEN_URL, headers=headers, data=args)
        token = r.json()

        try:
            access_token = token['access_token']
            refresh_token = token['refresh_token']
        except Exception as e:
            return None

        # update user info every time they authenticate so it stays in sync.
        wa_user = utils.get_wa_user_for_account('me', token=access_token, create=True, update=True)
        # make sure user was not deactivated
        if (not wa_user) or (not wa_user.user.is_active):
            return None
        # set access and refresh tokens
        wa_user.access_token = access_token
        wa_user.refresh_token = refresh_token
        wa_user.save()

        return wa_user.user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
