from rest_framework import serializers
from api import utils
from api.models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'email', 'phone', 'gender', 'ntrp', 'user', 'flight', 'league')

class PlayerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'gender', 'ntrp', 'user', 'flight', 'league')
        read_only_fields = fields

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'league', 'name', 'year', 'ntrp', 'start_date')

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'year')

class MatchPublicSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)
    home_player = PlayerPublicSerializer(read_only=True)
    visitor_player = PlayerPublicSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ('id', 'flight', 'year', 'status', 'home_player', 'visitor_player', 'score', 'winner', 'scheduled_date', 'played_date', 'entry_date')
        # all fields are read-only
        read_only_fields = fields

class MatchPlayerSerializer(serializers.ModelSerializer):
    """Serializer to be used for (non-admin) player score entry

    Players can only write to a small subset of all Match fields.
    """
    # Related model serializers
    flight = FlightSerializer(read_only=True)
    home_player = PlayerPublicSerializer(read_only=True)
    visitor_player = PlayerPublicSerializer(read_only=True)

    # Non-default field serializers
    # update entry date to "now" whenever an updated is submitted
    entry_date = serializers.DateField(read_only=True, default=utils.today)
    # require played_date, status, winner, score
    played_date = serializers.DateField(required=True)
    status = serializers.ChoiceField(choices=Match.Statuses, required=True)
    winner = serializers.ChoiceField(choices=Match.Winners, required=True)
    # don't require score in case it's a default
    score = serializers.CharField(max_length=63, required=False)

    def validate(self, data):
        score = data.get('score')
        if data['winner'] == Match.DBL_DEFAULT:
            if data['status'] != Match.DEFAULT:
                raise serializers.ValidationError('Match status must be "default" for double default match')
            else:
                # special case. no one gets points.
                score = '0-0'
        elif data['status'] == Match.DEFAULT:
            # default is always 10-0 (unless it's a double default)
            score = '10-0'
        if not score:
            # Score must be set by now
            raise serializers.ValidationError('score cannot be empty')
        if data['status'] == 'completed':
            # validate score only if match was completed
            try:
                utils.is_valid_score(score, best_of=1, set_games=10)
            except Exception as e:
                raise serializers.ValidationError(str(e))

        # always normalize score, even if not completed.
        try:
            data['score'] = utils.normalize_score(score)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return data

    class Meta:
        model = Match
        fields = ('id', 'flight', 'year', 'status', 'home_player', 'visitor_player', 'score', 'winner', 'scheduled_date', 'played_date', 'entry_date')
        # writable_fields is just a convenience for calculating read_only_fields based on the difference.
        writable_fields = ('status', 'score', 'winner', 'played_date')
        read_only_fields = tuple(set(fields) - set(writable_fields))

