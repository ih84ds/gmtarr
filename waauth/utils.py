import requests, json

from django.conf import settings
from waauth.models import WAUser

def api_call_get(api_path, access_token, args=None):
	headers = {
	    'authorization': 'Bearer {}'.format(access_token)
	}
	r = requests.get('{}/{}'.format(settings.WA_API_URL, api_path), headers=headers, data=args)
	return r.json()

def get_contact_info(wa_user_id, access_token):
	api_path = 'Accounts/{}/Contacts/me'.format(wa_user_id)
	return api_call_get(api_path, access_token)