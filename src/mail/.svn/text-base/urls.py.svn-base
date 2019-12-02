# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('newtype.mail.views',
	(r'^count_unread/$', 'count_unread'),
	(r'^send_mail/$', 'send_mail'),		# user send mail ,	type=<number>  (1,u'basic message & alerting'),(2,u'invitation from union'),(3,u'gift'), (4,u'first step of trade'),
						#			send_to=<string> (u'player',u'player'),(u'union',u'union'),
						#			target_name=<string>  name of player or name of union
						#			subject=<string>
						#			message=<string>
						#			item_list=[item id]
						#			money=<int>
						# return  <String> Result
	(r'^show_inbox/$', 'show_inbox'),
						# return <JSON> [{
						#		'id'		:e.id,
						#		'type'		:e.type,
						#		'subject'	:e.subject,
						#		'sender'	:str(e.get_sender()),
						#		'send_at'	:str(e.send_at),
						#		'unread'	:e.unread
						#		},{},{}]
	(r'^show_waiting/$', 'show_waiting'),
						# return <JSON> [{
						#		'id'		:e.id,
						#		'type'		:e.type,
						#		'subject'	:e.subject,
						#		'receiver'	:str(e.get_receiver()),
						#		'send_at'	:str(e.send_at)
						#		},{},{}]
	(r'^read_mail/$', 'read_mail'),		#			mail_id=<number>
						# return <JSON>	error_message	<string or blank string >
						#		type	<string>
						#		waiting	<bool>	if true -> show cancel button
						#		subject	<string>
						#		message	<string>
						#		sender	<string>
						#		send_at	<string>
						#		item1	<object standard item>
						#		money1	<number>
						#		item2	<object standard item>
						#		money2	<number>
	(r'^answer_trade/$', 'answer_trade'),	# has been trade step 1
						#			mail_id=<number>
						#			message=<string>
						#			item_list=[item id]
						#			money=<number>
						# return <String>
	(r'^accept/$', 'accept'),		#			mail_id=<number>
						# return <String>
	(r'^decline/$', 'decline'),		#			mail_id=<number>
						# return <String>
)
