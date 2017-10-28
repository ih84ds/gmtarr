import datetime, json, math, re
from django.utils import timezone
from waauth import utils as wautils
from api.models import *

def create_balanced_round_robin(players):
    """ Create a schedule for the players in the list and return it"""
    s = []
    if len(players) % 2 == 1: players = players + [None]
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

def create_league_for_event(token, event_id):
    try:
        league = League.objects.get(event_id=event_id)
        raise Exception('League "{}" already exists for event {}.'.format(league.name, event_id))
    except League.DoesNotExist as e:
        event = wautils.get_rr_event_info(token, event_id)
        league = League(event_id=event_id)
        league.year = datetime.date.today().year
        if event['Name']:
            league.name = event['Name']
        else:
            league.name = 'League for Event {}'.format(event_id)
        league.save()

    return league

def format_phone(phone, format='{}-{}-{}'):
    nanp = re.compile('([2-9][0-9]{2})([^0-9]*)([2-9][0-9]{2})([^0-9]*)([0-9]{4})')
    m = nanp.match(phone)
    if m:
        phone = format.format(m.group(1), m.group(3), m.group(5))
    return phone

def format_set_score(score):
    set_regex = re.compile('^\s*([0-9]+)\s*-\s*([0-9]+)\s*(?:\(([0-9]+)\)\s*)?$')
    m = set_regex.match(score)
    if not m:
        raise Exception('indecipherable set score: {}'.format(score))
    if m.group(3):
        score = '{}-{}({})'.format(m.group(1), m.group(2), m.group(3))
    else:
        score = '{}-{}'.format(m.group(1), m.group(2))
    return score

def generate_matches_for_flight(flight, match_timedelta=None):
    players = list(flight.players.all())
    schedule = create_balanced_round_robin(players)
    match_date = flight.start_date
    if not match_timedelta:
        match_timedelta = datetime.timedelta(weeks=1)
    for round in schedule:
        for p1, p2 in round:
            if not p1 or not p2:
                continue
            match = Match()
            match.flight = flight
            match.year = flight.year
            match.home_player = p2
            match.visitor_player = p1
            if match_date:
                match.scheduled_date = match_date
            match.save()
        if match_date:
            match_date += match_timedelta

def import_players_for_event(token, league, event_id):
    registrants = wautils.get_rr_event_registrants(token, event_id)

    players = []
    for r in registrants:
        wa_user = wautils.get_wa_user_for_account(r['contact_id'], token=token, create=True)
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

def is_valid_score(score, best_of=1, set_games=10):
    # normalize score string so we don't have to over-complicate our regexes
    score = normalize_score(score)
    match_regex = re.compile('[0-9]+-[0-9]+(?:\([0-9]+\))?')
    set_regex = re.compile('([0-9]+)-([0-9]+)(?:\(([0-9]+)\))?')
    sets = match_regex.findall(score)
    min_sets = math.ceil(best_of / 2)
    max_sets = best_of
    if len(sets) < min_sets or len(sets) > max_sets:
        # wrong number of sets
        raise Exception('wrong number of sets: {}'.format(len(sets)))
    winner_sets_won = 0
    for set in sets:
        m = set_regex.match(set)
        match_winner_score = int(m.group(1))
        match_loser_score = int(m.group(2))
        set_winner_score = max(match_winner_score, match_loser_score)
        set_loser_score = min(match_winner_score, match_loser_score)
        if set_winner_score == match_winner_score:
            winner_sets_won += 1
        if set_winner_score > (set_games + 1) or (set_winner_score > set_games and set_loser_score < (set_games - 1)):
            # too many games played
            raise Exception('too many games played: {}'.format(set))
        if set_winner_score < set_games:
            # too few games played
            raise Exception('not enough games played: {}'.format(set))
        if not (set_winner_score >= (set_loser_score + 2) or (set_loser_score == set_games and set_winner_score == (set_games + 1))):
            # must win by 2 or win by 1 (tiebreaker) if max games were played
            raise Exception('must win by two: {}'.format(set))
        if m.group(3) is not None and not (set_winner_score == (set_games + 1) and set_loser_score == set_games):
            # can't have tiebreaker if max games were not played
            raise Exception('tiebreaker score entered for non-tiebreaker set: {}'.format(set))
    if winner_sets_won < min_sets:
        # winner didn't win minimum number of sets
        raise Exception('match winner did not win enough sets: {}'.format(score))
    return True

def normalize_score(score):
    sets = score.split(',')
    normalized_sets = []
    for set in sets:
        normalized_sets.append(format_set_score(set))
    return ', '.join(normalized_sets)

def today():
    return timezone.localdate()
