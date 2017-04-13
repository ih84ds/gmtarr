from rest_framework import serializers
from api.models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'email', 'phone', 'gender', 'ntrp', 'flight_id', 'league_id')

class PlayerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'gender', 'ntrp', 'flight_id', 'league_id')

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'league_id', 'name', 'year', 'ntrp', 'start_date')

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'year')
