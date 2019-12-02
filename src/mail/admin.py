# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.html import escape
from newtype.mail.models import Mail

class MailAdmin(admin.ModelAdmin):
	list_display = ('id', 'type', 'subject' ,'get_sender', 'get_receiver')

admin.site.register(Mail,MailAdmin)
#admin.site.register(Players_Items_Mails)

