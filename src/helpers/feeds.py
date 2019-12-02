# -*- coding: UTF-8 -*-
from newtype.core.models import Player,ServerStatus,Items_HoldEffects,Effect
from newtype.mail.views import send_alert
from newtype.helpers.engine import execute_effect
import urllib
import math
import random
from xml.dom import minidom
from django.core.exceptions import ObjectDoesNotExist

CANNOT_DESTROY_TYPE = set([u'เทคโนโลยี',u'ขยะ'])

def earthquake():
	world_disaster_modifier=float(ServerStatus.objects.get(name='disaster_modifier').value)
	data=urllib.urlopen('http://earthquake.usgs.gov/earthquakes/catalogs/eqs1hour-M1.txt').read()
	# print data
	data=data.split('\r\n')
	first=True
	for e in data:
		detail=e.split(',')
		if len(detail)<=1:
			break
		if first:
			first=False
		else:
			latitude=float(detail[6])
			longitude=float(detail[7])
			magnitude=float(detail[8])
			region=detail[11]
			queryset=Player.objects.all()
			for e in queryset:
				if math.sqrt((e.latitude-latitude)**2 + (e.longitude-longitude)**2) < magnitude*2 :
					#check active effect (do not have now)
					try:
						disaster_modifier=e.activeeffect_set.get(effect__name='disaster_modifier')
						rate=int(eval(disaster_modifier.value)['rate'])
					except ObjectDoesNotExist:
						rate=100
					
					all_item=e.items.all()
					for item in all_item:
						all_hold_effect=item.hold_effects.all()
						for hold_effect in all_hold_effect:
							if hold_effect.effect.name=='disaster_modifier':
								rate=rate*int(eval(hold_effect.value)['rate'])/100
					
					destroy_rate=(magnitude/10)*(rate/100)*world_disaster_modifier
					was_destroy=False
					all_item=e.ownership_set.all()
					for item in all_item:
						# print type(item)
						if (random.random()*100) < destroy_rate and  len(set(item.item.get_item_types_list()) & CANNOT_DESTROY_TYPE)==0 :
							item.delete()		#if delete selling item, that sell will be deleted automaticly
							was_destroy=True
					if was_destroy:
						send_alert(e,u'ภัยพิบัติ',u'แผ่นดินไหว ความแรงขนาด '+unicode(magnitude)+u'ริกเตอร์ ที่ '+region+u' ทำให้ไอเทมบางส่วนของคุณเสียหาย')
	return True

def big_disaster():
	for player in Player.objects.all():
		destroy_rate=50
		was_destroy=False
		all_item=player.ownership_set.all()
		for item in all_item:
			#print type(item)
			if (random.random()*100) < destroy_rate and  len(set(item.item.get_item_types_list()) & CANNOT_DESTROY_TYPE)==0 :
				item.delete()		#if delete selling item, that sell will be deleted automaticly
				was_destroy=True
		if was_destroy:
			send_alert(player,u'อภิมหาภัยพิบัติ',u'โลกเกิดภัยพิบัติครั้งยิ่งใหญ่ เนื่องจากโลกเสียสมดุลย์จากการกระทำของมนุษย์ ทำให้ทรัพย์สินของคุณเสียหายไปมาก')
	return True

def weather_to_id(word):
	word=word.lower()
	if ('sun' in word):
		return '1'
	elif ('cloud' in word ) or ('hazy' in word ):
		return '2'
	elif ('rain' in word) or ('wind' in word) or ('humid' in word ):
		return '3'
	elif ('snow' in word) or ('cold' in word)  or ('flurry' in word):
		return '4'
	else:
		return '1'		#I do not know the all word of weather from weatherbug.com

def feed_weather():
	dom = minidom.parse(urllib.urlopen('http://a3333436343.api.wxbug.net/getLiveWeatherRSS.aspx?ACode=A3333436343&cityCode=75672&OutputType=1&UnitType=1'))
	
	this_weather_id=ServerStatus.objects.get(name='weather_id')
	this_weather_id.value=weather_to_id(dom.getElementsByTagName('aws:current-condition')[0].firstChild.data)
	this_weather_id.save()

	this_wind_speed=ServerStatus.objects.get(name='wind_speed')
	this_wind_speed.value=dom.getElementsByTagName('aws:wind-speed')[0].firstChild.data
	this_wind_speed.save()

	this_temperature=ServerStatus.objects.get(name='temperature')
	this_temperature.value=dom.getElementsByTagName('aws:temp')[0].firstChild.data
	this_temperature.save()

	this_rain_rate=ServerStatus.objects.get(name='rain_rate')
	this_rain_rate.value=dom.getElementsByTagName('aws:rain-rate')[0].firstChild.data
	this_rain_rate.save()
	
	return True
#print dom.getElementsByTagName('aws:aux-temp')[0].firstChild.data
#print dom.getElementsByTagName('aws:aux-temp')[0].getAttribute('units')

def fill_clean_energy():
	weather_id=int(ServerStatus.objects.get(name='weather_id').value)
	temperature=float(ServerStatus.objects.get(name='temperature').value)
	rain_rate=float(ServerStatus.objects.get(name='rain_rate').value)
	wind_speed=float(ServerStatus.objects.get(name='wind_speed').value)
	for player in Player.objects.all():
		for item in player.items.all():
			for hold_effect in item.hold_effects.all():
				if hold_effect.effect.name=='generate_clean_energy':
					data=eval(hold_effect.effect.value)
					if data['type']=='solar':
						if weather_id==1 :
							energy=int(data['magnitude']*temprature*2)
					elif data['type']=='water':
						energy=int(data['magnitude']*rain_rate)
					elif data['type']=='wind':
						energy=int(data['magnitude']*wind_speed)
					player.replenish_mechanical_energy(energy)
	return True

def random_disease():
	disease = Effect.objects.get(name='regis_disease')
	value = '''{
				'regis_effect': 'disease',
				'chance': ''' + ServerStatus.objects.get(name='disease_chance').value + ''',
				'expiration': datetime.timedelta(days=3),
				'data': {
					'max_energy': -1,
					'regeneration_rate': -1,
					'research_cost': +1,
					'travel_cost': +1,
				},
			}'''
	for player in Player.objects.all():
		execute_effect(effect=disease, request=None, value=value, player=player)
	return True
