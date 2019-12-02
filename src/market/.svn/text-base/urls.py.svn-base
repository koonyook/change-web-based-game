# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('newtype.market.views',
    # Example:
    # (r'^newtype/', include('newtype.foo.urls')),
    (r'^search_in_sell/$', 'search_in_sell'),		# GET , POST 
							#	item_name=<string>
							#	level=<number>
							#	sort_by=<string> 'price' or 'level'
							# return <JSON>
							#	{
							#		'id'		:e.id,
							#		'price'		:e.price,
							#		'expire_at'	:str(e.expire_at),
							#		'level'		:e.item.level,
							#		'durability':e.item.durability,
							#		'item_name'	:e.item.item.name,
							#		'icon_url'	:e.item.item.icon_url,
							#		'max_durability':e.item.item.durability,
							#		'storage_cost':e.item.item.storage_cost,
							#		'seller'	:str(e.item.get_owner()),
							#		'cancle_button':cancle_button
							#	}
	(r'^search_in_buy/$', 'search_in_buy'),		# GET , POST 
							#	item_name=<string>
							#	level=<number>
							#	can_sell=<bool>	True -> filter item in player have
							#	sort_by=<number>
							# return <JSON>
							#	{
							#		'id'		:e.id,
							#		'price'		:e.price,
							#		'expire_at'	:str(e.expire_at),
							#		'level'		:e.item.level,
							#		'item_name'	:e.item.item.name,
							#		'icon_url'	:e.item.item.icon_url,
							#		'quantity'	:e.quantity,
							#		'buyer'		:str(e.get_buyer()),
							#		'must_complete':e.must_complete,	True -> need durability 100% ?
							#		'cancle_button':cancle_button
							#	}
	(r'^new_sell/$', 'new_sell'),			# POST
							#	item_id=<number>
							#	price=<number>
							# return <String>
	(r'^new_buy/$', 'new_buy'),			# POST
							#	price=<number>	Full price
							#	item_id=<number>
							#	level=<number> at least lvl
							#	quantity=<number>
							#	must_complete=<number>
							# return <String>
	(r'^can_buy/$', 'can_buy'),			# GET
							# return <JSON> []
							# {
							#	id
							#	name
							# }
	(r'^player_buy/$', 'player_buy'),		# POST
							#	sell_id=<number>
							# return <String>
	(r'^player_sell/$', 'player_sell'),		# POST
							#	buy_id=<number>
							#	item_id=<number>
	(r'^cancel_sell/$', 'cancel_sell'),		# POST
							#	sell_id=<number>
	(r'^cancel_buy/$', 'cancel_buy'),		# POST
							#	buy_id=<number>
	(r'^sell_bank/$', 'sell_bank'),			# POST
							#	item_id=<number>
							# return <String>
	(r'^show_sell_patent/$', 'show_sell_patent'),	# POST
							# return <JSON>
							#	{
							#		'sell_id'	:e.id,								# use with buy_patent
							#		'patent_id'	:e.patent.id,						# use with read_patent to show detail
							#		'name'		:e.patent.formula.name,
							#		'seller'	:str(e.patent.get_owner()),
							#		'cancle_button':cancle_button
							#	}
	(r'^can_sell_patent/$', 'can_sell_patent'),	# POST
							# return <JSON>
							#	{
							#		'patent_id'	:e.id,						
							#		'name'		:e.formula.name
							#	}
	(r'^new_sell_patent/$', 'new_sell_patent'),	# POST
							#	price=<number>
							#	patent_id=<number>
							# return <String>
	(r'^buy_patent/$', 'buy_patent'),		# POST
							#	sell_patent_id=<number>
							# return <String>
	(r'^cancel_sell_patent/$', 'cancel_sell_patent'),# POST
							#	sell_patent_id=<number>
							# return <String>

    (r'^list/$', 'dbug'),
)
