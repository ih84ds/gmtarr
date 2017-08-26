import requests, json, base64

from django.conf import settings
from django.contrib.auth.models import User
from waauth.models import WAUser

def api_call_get(api_path, token, args=None):
    headers = {
        'authorization': 'Bearer {}'.format(token)
    }
    r = requests.get('{}/{}'.format(settings.WA_API_URL, api_path), headers=headers, params=args)
    return r.json()

def create_wa_user_for_account(token, contact_id, update_user=False, contact_info=None):
    if not contact_info:
        contact_info = get_contact_info(token, contact_id)
    try:
        # check for existing user
        user = User.objects.get(username=contact_info['Email'])
    except Exception as e:
        # create new user
        user = User()

    if (user.pk is None) or update_user:
        user.username = contact_info['Email']
        user.email = contact_info['Email']
        user.first_name = contact_info['FirstName']
        user.last_name = contact_info['LastName']
        user.save()

    wa_user = WAUser(user=user, wa_id=contact_info['Id'])
    wa_user.name = '{} {}'.format(contact_info['FirstName'], contact_info['LastName'])
    wa_user.save()
    return wa_user

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

def get_contact_info(token, wa_contact_id='me'):
    if wa_contact_id:
        api_path = 'Accounts/{}/Contacts/{}'.format(settings.WA_ACCOUNT_ID, wa_contact_id)

    return api_call_get(api_path, token)

def get_rr_events(token):
    api_path = 'Accounts/{}/Events'.format(settings.WA_ACCOUNT_ID)
    args = {
        '$filter': 'Tags in [round-robin]',
    }
    try:
        data = api_call_get(api_path, token, args=args)
        # Events is a subkey of the results for some reason.
        events = data['Events']
    except Exception as e:
        events = None
    return events

def get_rr_event_info(token, event_id):
    api_path = 'Accounts/{}/Events/{}'.format(settings.WA_ACCOUNT_ID, event_id)
    args = {
    }
    data = api_call_get(api_path, token, args=args)
    return data

def get_rr_event_registrants(token, event_id, normalize=True):
    api_path = 'Accounts/{}/EventRegistrations'.format(settings.WA_ACCOUNT_ID)
    args = {
        'eventId': event_id,
    }
    data = api_call_get(api_path, token, args=args)
    if not normalize:
        return data
    registrants = []
    for r in data:
        registrants.append(normalize_registrant_info(r))
    return registrants

def get_wa_user_for_account(contact_id, token=None, create=False, update=False, contact_info=None):
    if contact_id == 'me':
        if not contact_info:
            if not token:
                # can't determine account id for 'me' if we don't have a token
                return None
            contact_info = get_contact_info(token, contact_id)
        contact_id = contact_info['Id']

    try:
        wa_user = WAUser.objects.get(wa_id=contact_id)
    except WAUser.DoesNotExist:
        wa_user = None

    if not wa_user:
        if (not create) or (not token):
            return None
        elif create:
            return create_wa_user_for_account(token, contact_id, update_user=update, contact_info=contact_info)

    if update and token:
        wa_user = update_wa_user_for_account(wa_user, token, contact_id, contact_info=contact_info)

    return wa_user

def normalize_registrant_info(data):
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
            if info_key == 'gender':
                field_value = field_value.lower()
                if field_value.startswith('m'):
                    field_value = 'male'
                elif field_value.startswith('f'):
                    field_value = 'female'
                else:
                    field_value = None
            info[info_key] = field_value
    return info

def update_wa_user_for_account(wa_user, token, contact_id, contact_info=None):
    if not contact_info:
        contact_info = get_contact_info(token, contact_id)
    user = wa_user.user
    user.username = contact_info['Email']
    user.email = contact_info['Email']
    user.first_name = contact_info['FirstName']
    user.last_name = contact_info['LastName']
    user.save()
    wa_user.name = '{} {}'.format(contact_info['FirstName'], contact_info['LastName'])
    wa_user.wa_id = contact_info['Id']
    wa_user.save()
    return wa_user
