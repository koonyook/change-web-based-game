# -*- coding: UTF-8 -*-
from newtype.core.models import Player,Union

def get_person_request(request):
	if request.session.get('state')=='player':
		return request.user.player
	elif request.session.get('state')=='union':
		return request.user.player.union
	else:
		return None

def get_person_raw(type,name):			#return object of player or union #type='player' or 'union' #name is name
	if (type=='player'):
		try:
			return Player.objects.get(user__username=name)
		except ObjectDoesNotExist:
			return None
	else:
		try:
			return Union.objects.get(name=name)	
		except ObjectDoesNotExist:
			return None