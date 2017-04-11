import requests, json, base64

from django.conf import settings
from waauth.models import WAUser

def api_call_get(api_path, access_token, args=None):
    headers = {
        'authorization': 'Bearer {}'.format(access_token)
    }
    r = requests.get('{}/{}'.format(settings.WA_API_URL, api_path), headers=headers, params=args)
    return r.json()

def get_api_auth_token():
    args = {
        'grant_type': 'client_credentials',
        'scope': 'auto',
    }

    access_header_raw = '{}:{}'.format('APIKEY', settings.WA_API_KEY)
    authorization_header = base64.b64encode(access_header_raw.encode()).decode()
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'authorization': 'Basic {}'.format(authorization_header)
    }

    r = requests.post(settings.WA_TOKEN_URL, headers=headers, data=args)
    token = r.json()
    return token

def get_contact_info(access_token, wa_user_id):
    api_path = 'Accounts/{}/Contacts/me'.format(wa_user_id)
    return api_call_get(api_path, access_token)

def get_rr_events(api_auth_token):
    api_path = 'Accounts/{}/Events'.format(settings.WA_ACCOUNT_ID)
    args = {
        '$filter': 'Tags in [round-robin]',
    }
    try:
        data = api_call_get(api_path, api_auth_token, args=args)
        # Events is a subkey of the results for some reason.
        events = data['Events']
    except Exception as e:
        events = None
    return events

def get_rr_event_registrants(api_auth_token, event_id):
    api_path = 'Accounts/{}/EventRegistrations'.format(settings.WA_ACCOUNT_ID)
    args = {
        'eventId': event_id,
    }
    data = api_call_get(api_path, api_auth_token, args=args)
    registrants = []
    for r in data:
        registrants.append(get_rr_event_registrant_info(r))
    return registrants

def get_rr_event_registrant_info(data):
    info = {
        'contact_name': data['Contact']['Name'],
        'contact_id': data['Contact']['Id'],
        'registration_date': data['RegistrationDate'],
    }
    fields_map = {
        'First name': 'first_name',
        'Last name': 'last_name',
        'Email': 'email',
        'Phone': 'phone',
        'Gender': 'gender',
        'NTRP Level': 'ntrp',
    }
    for field in data['RegistrationFields']:
        field_name = field['FieldName']
        if field_name in fields_map:
            info_key = fields_map[field_name]
            field_value = field['Value']
            if isinstance(field_value, dict):
                # choice values end up being an array { Id: xxxx, Label: actual_value }
                field_value = field_value['Label']
            info[info_key] = field_value
    return info