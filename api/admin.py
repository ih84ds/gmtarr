from django.contrib import admin
from api.models import *

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_filter = ('year', 'event_id')
    search_fields = ('name', )
    
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_filter = ('year', 'league', 'ntrp', 'start_date')
    search_fields = ('name', )
    
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_filter = ('gender', 'ntrp', 'league', 'flight')
    search_fields = ('name', 'email')
    
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_filter = ('year', 'flight__league', 'flight', 'scheduled_date', 'status')
    search_fields = ('home_player__name', 'visitor_player__name')
    
