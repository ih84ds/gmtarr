from rest_framework import serializers
from api.models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'email', 'phone', 'gender', 'ntrp', 'flight', 'league')

class PlayerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'gender', 'ntrp', 'flight', 'league')

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'league', 'name', 'year', 'ntrp', 'start_date')

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'year')

class MatchPublicSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()
    home_player = PlayerPublicSerializer()
    visitor_player = PlayerPublicSerializer()

    class Meta:
        model = Match
        fields = ('id', 'flight', 'year', 'status', 'home_player', 'visitor_player', 'score', 'winner', 'scheduled_date', 'played_date', 'entry_date')
