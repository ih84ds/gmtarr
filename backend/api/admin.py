from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
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
    list_display = ('name', 'gender', 'ntrp', 'league', 'flight')
    search_fields = ('name', 'email')
    actions = ['set_flight']

    class FlightForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        flight = forms.ModelChoiceField(Flight.objects)

    def set_flight(self, request, queryset):
        form = self.FlightForm(request.POST)
        if 'apply' in request.POST:
            if form.is_valid():
                flight = form.cleaned_data['flight']
                count = 0
                for player in queryset:
                    player.flight = flight
                    player.save()
                    count += 1
                plural = 's' if count > 1 else ''
                self.message_user(request, u'Successfully set Flight {} for {} player{}.'.format(flight, count, plural))
                return redirect(request.get_full_path())
        context = {
            'players': queryset,
            'form': form,
        }
        return render(request, 'set_flight.html', context)
    set_flight.short_description = 'Bulk Set Flight'
    
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_filter = ('year', 'flight__league', 'flight', 'scheduled_date', 'status')
    search_fields = ('home_player__name', 'visitor_player__name')
    
