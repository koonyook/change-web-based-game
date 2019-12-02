# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.html import escape
from newtype.core.models import Union, Item, ItemType, Items_HoldEffects, Items_UseEffects, ServerStatus, Effect, EffectType, Location, Formula, Formulas_Effects, Harvesting, Rarity, Player, Result, ActiveEffect, ResearchLog
from newtype.patent.models import Patent
from newtype.core_union.models import SettingUnion

class Items_HoldEffectsInline(admin.TabularInline):
    model = Items_HoldEffects
    extra = 2
    
class Items_UseEffectsInline(admin.TabularInline):
    model = Items_UseEffects
    extra = 2
    
class ResultInline(admin.TabularInline):
    model = Result
    extra = 5

class RarityInline(admin.TabularInline):
    model = Rarity
    extra = 4

class HarvestingInline(admin.TabularInline):
    model = Harvesting

class PatentInline(admin.TabularInline):
    model = Patent

class Formulas_EffectsInline(admin.TabularInline):
    model = Formulas_Effects

class SettingUnionInline(admin.TabularInline):
    model = SettingUnion

class ItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon_url', 'image_url', 'item_types'),
        }),
        ('Properties', {
            'fields': (('storage_cost', 'expiration', 'durability', 'price'),),
        }),
        ('Pollution', {
            'fields': (('air_pollution', 'water_pollution', 'earth_pollution'),),
        }),
        ('Modifiers', {
            'fields': (('storage_modifier', 'harvest_cost_modifier', 'max_energy_modifier', 'max_mechanical_energy_modifier', 'travel_cost_modifier', 'research_cost_modifier', 'research_modifier', 'regeneration_rate_modifier'), ),'classes': ['collapse']
        }),
    )
    inlines = [Items_UseEffectsInline, Items_HoldEffectsInline, RarityInline, HarvestingInline]
    list_display = ('id','name','description','icon_url','get_image_tag')
    list_editable = ('icon_url',)
    search_fields = ['name', 'description']
    save_as = True
    
class FormulaAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Ingredients', {
           'fields': (('components', 'component_types',), 'weather'),
        }),
    )
    inlines = [ResultInline , Formulas_EffectsInline, PatentInline]
    radio_fields = {'weather': admin.HORIZONTAL}
    search_fields = ['name', 'description']
    save_as = True
    list_display = ('id','name', 'description','get_component','get_all_result')

class PlayerAdmin(admin.ModelAdmin):
    inlines = [SettingUnionInline]

class EffectAdmin(admin.ModelAdmin):
    list_display = ('id','name','effect_type','value')

class ServerStatusAdmin(admin.ModelAdmin):
    list_display = ('name','value')
    list_editable = ('value',)

class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name','get_all_item')

class HarvestingAdmin(admin.ModelAdmin):
    list_display = ('id','unlocker','get_all_item')

class ResearchLogAdmin(admin.ModelAdmin):
    list_display = ('id','get_owner','formula','weather','time')

# Register models to admin site here
admin.site.register(Player,PlayerAdmin)
admin.site.register(Union)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ServerStatus, ServerStatusAdmin)
admin.site.register(Effect, EffectAdmin)
admin.site.register(EffectType)
admin.site.register(ActiveEffect)
admin.site.register(Location)
admin.site.register(Formula, FormulaAdmin)
admin.site.register(Harvesting, HarvestingAdmin)
admin.site.register(Rarity)

#Koon want to use this for debugging
from newtype.core.models import Ownership
admin.site.register(Ownership)
admin.site.register(ResearchLog,ResearchLogAdmin)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('item','formula')
admin.site.register(Result,ResultAdmin)

class Items_EffectsAdmin(admin.ModelAdmin):
    list_display = ('id','effect','value',)
    list_editable = ('value',)

admin.site.register(Items_HoldEffects,Items_EffectsAdmin)
admin.site.register(Items_UseEffects,Items_EffectsAdmin)
admin.site.register(Formulas_Effects,Items_EffectsAdmin)
