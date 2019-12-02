# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.html import escape
from newtype.patent.models import Patent

class PatentAdmin(admin.ModelAdmin):
	list_display = ('id','formula','regis_cost','copy_cost','status','get_owner')
	list_editable = ('regis_cost','copy_cost',)

admin.site.register(Patent, PatentAdmin)