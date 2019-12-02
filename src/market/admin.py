# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.html import escape
from newtype.market.models import Buy,Sell,SellPatent

class SellAdmin(admin.ModelAdmin):
	list_display = ('id', 'item_name', 'item_level', 'price', 'expire_at', 'seller')

class BuyAdmin(admin.ModelAdmin):
	list_display = ('id', 'item_name', 'level', 'price', 'expire_at', 'get_buyer')

class SellPatentAdmin(admin.ModelAdmin):
	list_display = ('id', 'patent', 'price', 'seller')

admin.site.register(Sell,SellAdmin)
admin.site.register(Buy,BuyAdmin)
admin.site.register(SellPatent,SellPatentAdmin)
 