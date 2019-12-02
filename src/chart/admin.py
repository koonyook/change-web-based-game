from django.contrib import admin
from newtype.chart.models import State

class StateAdmin(admin.ModelAdmin):
	list_display = ('id','time', 'air_pollution', 'water_pollution', 'earth_pollution', 'natural_resources', 'researches')
	list_editable = ('air_pollution', 'water_pollution', 'earth_pollution', 'natural_resources', 'researches')
	save_as = True
admin.site.register(State, StateAdmin)
