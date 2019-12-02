# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.html import escape
from newtype.core.models import Union, Player
from newtype.core_union.models import Forum,Reply,SettingUnion

class ReplyInline(admin.TabularInline):
	model = Reply
	extra = 1

class ForumAdmin(admin.ModelAdmin):
	list_display = ('id','union','subject')
	inlines = [ReplyInline]

admin.site.register(Forum, ForumAdmin)
#admin.site.register(SettingUnion)