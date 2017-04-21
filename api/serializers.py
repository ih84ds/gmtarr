from rest_framework import serializers
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
    flight = FlightSerializer(read_only=True)
    home_player = PlayerPublicSerializer(read_only=True)
    visitor_player = PlayerPublicSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ('id', 'flight', 'year', 'status', 'home_player', 'visitor_player', 'score', 'winner', 'scheduled_date', 'played_date', 'entry_date')
        # writable_fields is just a convenience for calculating read_only_fields based on the difference.
        writable_fields = ('status', 'score', 'winner', 'played_date')
        read_only_fields = tuple(set(fields) - set(writable_fields))
