from django.contrib import admin
from api.models import *

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass
    
