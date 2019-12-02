# -*- coding: UTF-8 -*-
from newtype.core.models import Ownership, Item
from newtype.helpers.trim_time import trim_time

def item_dict(e):		#from standard like shinz's request
	data=dict()
	if type(e)==Ownership:
		data ={
		'ownership_id': e.id,
		'durability': e.durability,
        'level'		: e.level,
		'expiration': trim_time(e.expire_at),
		'is_available': bool(e.is_available)
		}
		if data['expiration']=='None':
			data['expiration']=None
		item=e.item
	elif type(e)==Item:
		item=e
	else:
		return None

	data['item_id']=item.id
	data['name']=item.name
	data['description']=item.description
	data['image_url']=item.get_full_image_url()
	data['icon_url'	]=item.get_full_icon_url()
	data['max_durability']=item.durability	
	data['size']=item.storage_cost
	data['air_pollution']=item.air_pollution
	data['water_pollution']=item.water_pollution
	data['earth_pollution']=item.earth_pollution
	data['storage_modifier']=item.storage_modifier
	data['storage_cost']=item.storage_cost
	data['max_energy_modifier']=item.max_energy_modifier
	data['max_mechanical_energy_modifier']=item.max_mechanical_energy_modifier
	data['travel_cost_modifier']=item.travel_cost_modifier
	data['harvest_cost_modifier']=item.harvest_cost_modifier
	data['research_cost_modifier']=item.research_cost_modifier
	data['regeneration_rate_modifier']=item.regeneration_rate_modifier
	data['price']=item.price
	
	data['types']=[]
	for i in item.item_types.all():
		data['types'].append(i.name)
	return data