# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('newtype.patent.views',
    # Example:
    # (r'^newtype/', include('newtype.foo.urls')),
	(r'^show_all_patent/$', 'show_all_patent'),		# GET
								# return <JSON>
								#	{
								#		'id'		:e.id,
								#		'name'		:e.formula.name,
								#		'regis_at'	:str(e.regis_at),
								#		'founder'	:str(e.founder)
								#	}
	(r'^show_person_patent/$', 'show_person_patent'),	# POST
								#	view_by=<string> 'name' or 'union'
								#	{
								#		'id'		:e.id,
								#		'name'		:e.formula.name,
								#		'regis_at'	:str(e.regis_at)
								#	}
	(r'^read_patent/$', 'read_patent'),			# POST
								#	patent_id = '1'
								# return <JSON>
								#	{
								#		'error_message':'',
								#		'id'		:this_patent.id,
								#		'status'	0,1,2,3
								#		'owner'		:str(this_patent.get_owner()),
								#		'regis_at'	:str(this_patent.regis_at),
								#		'regis_cost':this_patent.regis_cost,
								#		'copy_cost'	:this_patent.copy_cost,
								#		'name'		:this_patent.formula.name,
								#		'description':this_patent.formula.description,
								#		'weather'	:str(this_patent.formula.weather)
								#		'component'	: how to combine
								#		'result'	: list of string
								#		'give_button'	: opensource or someone
								#	}
	(r'^open_patent/$', 'open_patent'),			# POST
								#	patent_id=<number>
								# return <String>
	(r'^give_patent/$', 'give_patent'),			# POST
								#	patent_id = <name>
								#	send_to = <string> 'player' or 'union'
								#	target_name = <string>
								# return <String>
	(r'^regis_patent/$', 'regis_patent'),			# POST
								#	regis_type = <string> 'regis' or 'open'
								#	patent_id = <number>
								# return <String>
)
