import datetime, json, re
from waauth import utils as wautils
from api.models import *

def create_balanced_round_robin(players):
    """ Create a schedule for the players in the list and return it"""
    s = []
    if len(players) % 2 == 1: players = players + ["BYE"]
    # manipulate map (array of indexes for list) instead of list itself
    # this takes advantage of even/odd indexes to determine home vs. away
    n = len(players)
    map = list(range(n))
    mid = n // 2
    for i in range(n-1):
        l1 = map[:mid]
        l2 = map[mid:]
        l2.reverse()
        round = []
        for j in range(mid):
            t1 = players[l1[j]]
            t2 = players[l2[j]]
            if j == 0 and i % 2 == 1:
                # flip the first match only, every other round
                # (this is because the first match always involves the last player in the list)
                round.append((t2, t1))
            else:
                round.append((t1, t2))
        s.append(round)
        # rotate list by n/2, leaving last element at the end
        map = map[mid:-1] + map[:mid] + map[-1:]
    return s

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
