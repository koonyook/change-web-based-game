# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.html import escape
from newtype.help.models import QuestionAnswer

class QuestionAnswerAdmin(admin.ModelAdmin):
	list_display = ('id', 'question', 'answer')

admin.site.register(QuestionAnswer,QuestionAnswerAdmin)