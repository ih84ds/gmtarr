import datetime, json, re
from waauth import utils as wautils
from api.models import *

def format_phone(phone, format='{}-{}-{}'):
    nanp = re.compile('([2-9][0-9]{2})([^0-9]*)([2-9][0-9]{2})([^0-9]*)([0-9]{4})')
    m = nanp.match(phone)
    if m:
        phone = format.format(m.group(1), m.group(3), m.group(5))
    return phone

def import_players_for_event(event_id, league_name=None):
    try:
        league = League.objects.get(event_id=event_id)
    except Exception as e:
        league = League(event_id=event_id)
        league.year = datetime.date.today().year
        if league_name is None:
            league.name = 'League for Event {}'.format(event_id)
        else:
            league.name = league_name
        league.save()

    token = wautils.get_api_auth_token()
    access_token = token['access_token']
    registrants = wautils.get_rr_event_registrants(access_token, event_id)
    players = []
    for r in registrants:
        wa_user = wautils.get_wa_user_for_account(r['contact_id'], token=access_token, create=True)
        p = Player()
        p.name = '{} {}'.format(r['first_name'], r['last_name'])
        p.email = r['email']
        p.phone = format_phone(r['phone'])
        p.gender = r['gender']
        p.ntrp = r['ntrp']
        p.user = wa_user.user
        p.league = league
        p.save()
        players.append(p)
    return players