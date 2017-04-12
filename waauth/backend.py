# Python
import requests, base64

# Django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Custom
from waauth.models import WAUser
import waauth.utils as utils

class WAAuthBackend:
    def authenticate(self, token=None, request=None):
        args = {
            'grant_type': 'authorization_code',
            'code': token,
            'client_id': settings.WA_CLIENT_ID,
            'redirect_uri': request.build_absolute_uri(reverse('authenticate')),
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
            account_id = token['Permissions'][0]['AccountId']
        except Exception as e:
            return None
        contact_info = utils.get_contact_info(access_token, account_id)

        try:
            wa_user = WAUser.objects.get(wa_id=account_id)
            user = wa_user.user
        except WAUser.DoesNotExist:
            # insert new user into the db
            try:
                user = User.objects.get(username=contact_info['Email'])
            except Exception as e:
                user = User()
            wa_user = WAUser(wa_id=account_id)

        # make sure user was not deactivated
        if not user.is_active:
            return None

        # update user info every time they authenticate so it stays in sync.
        user.username = contact_info['Email']
        user.email = contact_info['Email']
        user.first_name = contact_info['FirstName']
        user.last_name = contact_info['LastName']
        user.save()

        # set user in case it's a new object
        # (in which case we couldn't set it earlier because it doesn't get an id until save.)
        wa_user.user = user
        wa_user.access_token = access_token
        wa_user.refresh_token = refresh_token
        wa_user.save()

        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
