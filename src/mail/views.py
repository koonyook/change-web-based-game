# -*- coding: UTF-8 -*-
# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from newtype.helpers.http import JSONResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from newtype.helpers.decorators import post_or_redirect_to_front

from django.core.exceptions import ObjectDoesNotExist

from newtype.core.models import Player,Union,Ownership, Item
from newtype.mail.models import Mail

from newtype.helpers.person import get_person_request , get_person_raw
from newtype.helpers.item_dict import item_dict
from newtype.helpers.trim_time import trim_time

import datetime
import math

CANNOT_DEAL_TYPE = set([u'เทคโนโลยี',u'ขยะ'])

def appear(type,name):				#true or false
	if (type=='player'):
		try:
			Player.objects.get(user__username=name)			#not sure
			return True
		except ObjectDoesNotExist:
			return False
	else:
		try:
			Union.objects.get(name=name)			#not sure
			return True
		except ObjectDoesNotExist:
			return False

def is_available(item_id):				#true or false   (&check type that cannot change owner)
	try:
		item=Ownership.objects.get(id=item_id)
		if item.is_available and item.expire_at==None:
			intersected=set(item.item.get_item_types_list()) & CANNOT_DEAL_TYPE
			if len(intersected)==0:
				return True
			else:
				return False
		else:
			return False
	except ObjectDoesNotExist:
		return False

@post_or_redirect_to_front
def send_mail(request):
	type=request.POST.get('type','')
	send_to=request.POST.get('send_to','')
	target_name=request.POST.get('target_name','')
	subject=request.POST.get('subject','')
	message=request.POST.get('message','')
	item_list=request.POST.getlist('item_list')
	money=request.POST.get('money','')
	
	person_sender=get_person_request(request)

	if (type=='2'):
		send_to='player'
		if request.user.player.union==None or not request.user.player.settingunion.can_persuade:
			return JSONResponse(u'ขออภัย คุณไม่ได้รับอนุญาติให้เชิญผู้อื่นเข้ามาทำงานในบริษัท')

	#validate data
	if (not appear(send_to,target_name)):
		return JSONResponse(u'Sorry, do not have '+send_to+' '+target_name)
	
	if (subject==''):
		if (type=='1'):
			subject=u'ข้อความจาก '+person_sender.__unicode__()
		elif (type=='2'):
			subject=u'จดหมายเชิญจากบริษัท '+person_sender.__unicode__()
		elif (type=='3'):
			subject=u'ของขวัญจาก '+person_sender.__unicode__()
		elif (type=='4'):
			subject=u'ข้อเสนอจาก '+person_sender.__unicode__()
	if (message==''):
		if (type=='2'):
			message=u'บริษัท '+person_sender+u' ต้องการเชิญคุณไปร่วมเป็นส่วนหนึ่งของบริษัท คุณจะยอมรับข้อตกลงนี้หรือไม่?'
		else:
			message='<no message>'

	if (type=='3' or type=='4'):
		for item_id in item_list:
			if(not is_available(item_id)):
				return JSONResponse(u'ขออภัย ไอเทมบางอย่างของคุณไม่สามารถส่งได้')
		if (money==''):
			money='0'
		if (not money.isdigit()):
			return JSONResponse(u'ขออภัย ข้อมูลจำนวนเงินผิดพลาด กรุณากรอกใหม่')
		else:
			money=int(money)
		if (person_sender.money < money):
			return JSONResponse(u'ขออภัย คุณมีเงินไม่เพียงพอ')

	#end validate data
	person_receiver=get_person_raw(send_to,target_name)

	this_mail=Mail.objects.create(type=int(type),subject=subject,message=message)
	this_mail.set_sender(person_sender)
	this_mail.set_receiver(person_receiver)

	if (type=='1'):
		this_mail.waiting=False	

	if (type=='3' or type=='4'):
		this_mail.set_item(1,item_list)
		person_sender.money-=money
		person_sender.save()
		this_mail.money1=money
	
	this_mail.save()

	return JSONResponse(u'การส่งข้อความเสร็จสมบูรณ์')

def send_alert(person,subject,message):
	this_mail=Mail.objects.create(type=1,subject=subject,message=message)
	this_mail.set_receiver(person)

@post_or_redirect_to_front
def count_unread(request):
	view_by=request.session['state']
	
	if view_by=='player':
		queryset=Mail.objects.filter(send_to_player=request.user.player)		#not sure
	else:
		queryset=Mail.objects.filter(send_to_union=request.user.player.union)	#not sure
	
	all_unread=queryset.filter(unread=True).count()
	
	return JSONResponse(unicode(all_unread))

def cmp_unread_before(data1,data2): return int(data2['unread'])-int(data1['unread'])

@post_or_redirect_to_front
def show_inbox(request):
	view_by=request.session['state']
	
	if view_by=='player':
		queryset=Mail.objects.filter(send_to_player=request.user.player)		#not sure
	else:
		queryset=Mail.objects.filter(send_to_union=request.user.player.union)	#not sure
	
	queryset=queryset.order_by('-send_at')
	temp=queryset.select_related(depth=2)
	data=list()
	for e in temp:
		data.append({
			'id'		:e.id,
			'type'		:e.type,
			'subject'	:e.subject,
			'sender'	:unicode(e.get_sender()),
			'send_at'	:trim_time(e.send_at),
			'unread'	:e.unread
		})
	data.sort(cmp_unread_before)

	return JSONResponse(data)

@post_or_redirect_to_front
def show_waiting(request):
	view_by=request.session['state']

	if view_by=='player':
		queryset=Mail.objects.filter(send_by_player=request.user.player)		#not sure
	else:
		queryset=Mail.objects.filter(send_by_union=request.user.player.union)	#not sure
	
	queryset=queryset.filter(type__in=[2,3,4,5],waiting=1)
	queryset=queryset.order_by('send_at')
	temp=queryset.select_related(depth=2)
	data=list()
	for e in temp:
		data.append({
			'id'		:e.id,
			'type'		:e.type,
			'subject'	:e.subject,
			'receiver'	:unicode(e.get_receiver()),
			'send_at'	:trim_time(e.send_at)
		})
	return JSONResponse(data)
'''
def item_dict(e):		#from standard like shinz's request
	data ={
		'id'		:e.id,
		'name'		:e.item.name,
		'description':e.item.description,
		'image_url'	:e.item.image_url,
		'icon_url'	:e.item.icon_url,
		'durability':e.durability,
		'max_durability':e.item.durability,	
		'level'		:e.level,
		'expiration':e.expire_at,
		'size'		:e.item.storage_cost,
		'air_pollution':e.item.air_pollution,
		'water_pollution':e.item.water_pollution,
		'earth_pollution':e.item.earth_pollution,
		'storage_modifier':e.item.storage_modifier,
		'max_energy_modifier':e.item.max_energy_modifier,
		'max_mechanical_energy_modifier':e.item.max_mechanical_energy_modifier,
		'travel_cost_modifier':e.item.travel_cost_modifier,
		'harvest_cost_modifier':e.item.harvest_cost_modifier,
		'research_cost_modifier':e.item.research_cost_modifier,
		'regeneration_rate_modifier':e.item.regeneration_rate_modifier
	}
	data['types']=[]
	tmp=e.item.item_types.all()
	for i in tmp:
		data['types'].append(i.name)
	return data
'''
#@post_or_redirect_to_front
def read_mail(request):
	mail_id=request.POST.get('mail_id','')

	try:
		this_mail=Mail.objects.get(id=mail_id)
	except ObjectDoesNotExist:
		return JSONResponse({'error_message':u'ขออภัย ไม่พบข้อความนี้ใน server'})
	
	this_mail.unread=False
	this_mail.save()
	data={}
	data['error_message']=''
	data['type']=this_mail.type
	data['type_name']=this_mail.get_type_display()
	data['waiting']=this_mail.waiting		#this data is used to show some button or not, if waiting=False, This mail will show only delete_button
	data['subject']=this_mail.subject
	data['message']=this_mail.message.replace('\n','<br/>')
	data['sender']=unicode(this_mail.get_sender())
	data['send_at']=trim_time(this_mail.send_at)

	data['item1']=[]
	data['money1']=this_mail.money1
	data['item2']=[]
	data['money2']=this_mail.money2
	
	data['answer_trade_button']=False
	data['accept_button']=False
	person=get_person_request(request)
	if (person==this_mail.get_receiver()):	
		if this_mail.type==4:
			data['answer_trade_button']=True
		elif this_mail.type in [2,3,5]:
			data['accept_button']=True

	if this_mail.type==3 or this_mail.type==4 or this_mail.type==5:
		tmp=this_mail.get_item_list(1)
		for item_id in tmp:
			e=Ownership.objects.get(id=item_id)
			data['item1'].append(item_dict(e))
	
	if this_mail.type==5:
		tmp=this_mail.get_item_list(2)
		for item_id in tmp:
			e=Ownership.objects.get(id=item_id)
			data['item2'].append(item_dict(e))
	return JSONResponse(data)

@post_or_redirect_to_front
def answer_trade(request):
	mail_id=request.POST.get('mail_id','')
	message=request.POST.get('message','')
	item_list=request.POST.getlist('item_list')
	money=request.POST.get('money','')
	person_sender=get_person_request(request)
	try:
		this_mail=Mail.objects.get(id=mail_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบข้อความนี้ใน server'})

	for item_id in item_list:
		if(not is_available(item_id)):
			return JSONResponse({'success':False,'message':u'ขออภัย ไอเทมบางอย่างของคุณไม่สามารถส่งได้'})
	if (money==''):
		money='0'
	if (not money.isdigit()):
		return JSONResponse({'success':False,'message':u'ขออภัย ข้อมูลจำนวนเงินผิดพลาด กรุณากรอกใหม่'})
	else:
		money=int(money)
	if (person_sender.money < money):
		return JSONResponse({'success':False,'message':u'ขออภัย คุณมีเงินไม่เพียงพอ'})
	person_sender.money-=money
	person_sender.save()
	#swap direction
	this_mail.send_by_player,this_mail.send_to_player = this_mail.send_to_player,this_mail.send_by_player
	this_mail.send_by_union,this_mail.send_to_union   = this_mail.send_to_union,this_mail.send_by_union
	#set everything
	this_mail.type=5
	this_mail.subject='RE: '+this_mail.subject
	this_mail.message=message
	this_mail.send_at=datetime.datetime.now()
	this_mail.unread=True
	this_mail.waitting=True
	this_mail.money2=money
	this_mail.set_item(2,item_list)
	this_mail.save()
	return JSONResponse({'success':True,'message':u'การส่งข้อความเสร็จสมบูรณ์'})

@post_or_redirect_to_front
def accept(request):
	mail_id=request.POST.get('mail_id','')
	try:
		this_mail=Mail.objects.get(id=mail_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบข้อความนี้ใน server'})
	if this_mail.type==2:		#regis user in union   #must add checking condition in the future
		if request.user.player.union==None:
			send_alert(this_mail.get_sender(),u'มีสมาชิกใหม่ในบริษัท',unicode(this_mail.get_receiver())+u' ได้เข้าร่วมในบริษัทของคุณแล้ว')
			request.user.player.union=this_mail.send_by_union
			request.user.player.save()
			this_mail.delete()
			return JSONResponse({'success':True,'message':u'คุณกลายเป็นสมาชิกคนหนึ่งของบริษัท "'+request.user.player.union.name+u'" แล้ว!'})
		else:
			return JSONResponse({'success':False,'message':u'กรุณาออกจากบริษัทเดิมของคุณ ก่อนจะเข้าบริษัทนี้'})
	elif this_mail.type==3:		#transfer item and money
		#checking condition (item storage)
		if (this_mail.get_receiver().get_free_space()<this_mail.count_space(1) ):
			return JSONResponse({'success':False,'message':u'ขออภัย คุณมีพื้นที่ไม่พอสำหรับไอเทมเหล่านี้'})
		send_alert(this_mail.get_sender(),u'มีคนได้รับของขวัญของคุณแล้ว',unicode(this_mail.get_receiver())+u' ได้รับของขวัญของคุณไปแล้ว')
		receiver=this_mail.get_receiver()
		receiver.money+=this_mail.money1
		receiver.save()
		this_mail.transfer_items(1,receiver)
		this_mail.delete()
		return JSONResponse({'success':True,'message':u'คุณได้รับของขวัญทั้งหมด'})
	elif this_mail.type==5:
		#checking condition (item storage)
		if (this_mail.get_receiver().get_free_space()+this_mail.count_space(1)<this_mail.count_space(2) ):
			return JSONResponse({'success':False,'message':u'ขออภัย คุณมีพื้นที่ไม่พอสำหรับไอเทมเหล่านี้'})
		if (this_mail.get_sender().get_free_space()+this_mail.count_space(2)<this_mail.count_space(1) ):
			return JSONResponse({'success':False,'message':u'ขออภัย ผู้ที่ต้องการแลกไอเทมกับคุณมีพื้นที่ไม่พอสำหรับไอเทมที่คุณให้ กรุณาติดต่อผู้ที่ต้องการแลกไอเทมกับคุณ'})
		send_alert(this_mail.get_sender(),u'การแลกเปลี่ยนเสร็จสิ้น',unicode(this_mail.get_receiver())+u' ได้ยอมรับการแลกเปลี่ยนของคุณแล้ว')
		receiver=this_mail.get_receiver()
		sender=this_mail.get_sender()
		receiver.money+=this_mail.money2
		sender.money+=this_mail.money1
		receiver.save()
		sender.save()
		this_mail.transfer_items(1,sender)
		this_mail.transfer_items(2,receiver)
		this_mail.delete()
		return JSONResponse({'success':True,'message':u'การแลกเปลี่ยนเสร็จสิ้น'})
	else:
		return JSONResponse({'success':False,'message':u'คุณไม่สามารถยอมรับจดหมายชนิดนี้ได้'})

@post_or_redirect_to_front
def decline(request):				#this methon will also delete that mail
	mail_id=request.POST.get('mail_id','')
	
	try:
		this_mail=Mail.objects.get(id=mail_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบข้อความนี้ใน server'})

	person=get_person_request(request)
	# print request
	#print get_person_request(request)
	#print this_mail.get_sender()
	#print this_mail.get_receiver()
	if person==this_mail.get_receiver():
		decliner='receiver'
	elif person==this_mail.get_sender():
		decliner='sender'
	else:
		return JSONResponse({'success':False,'message':u'คุณไม่สามารถปฏิเสธ หรือลบจดหมายของผู้อื่นได้'})

	if this_mail.type==1:
		if decliner=='receiver':
			this_mail.delete()
			return JSONResponse({'success':True,'message':u'คุณได้ลบจดหมายนี้แล้ว'})
		else:
			return JSONResponse({'success':False,'message':u'คุณไม่สามารถลบจดหมายฉบับนี้ได้'})
	elif this_mail.type==2:
		if decliner=='receiver':
			send_alert(this_mail.get_sender(),u'การเชิญล้มเหลว',unicode(this_mail.get_receiver())+u' ได้ตอบปฏิเสธการเชิญเข้าบริษัทของคุณ')
		this_mail.delete()
		return JSONResponse({'success':True,'message':u'คุณได้ตอบปฏิเสธ และลบจดหมายฉบับนี้แล้ว'})
	elif this_mail.type==3 or this_mail.type==4:
		if decliner=='receiver':
			if this_mail.type==3:
				send_alert(this_mail.get_sender(),u'การให้ของขวัญล้มเหลว',unicode(this_mail.get_receiver())+u' ปฏิเสธการรับของขวัญจากคุณ')
			elif this_mail.type==4:
				send_alert(this_mail.get_sender(),u'การแลกเปลี่ยนไม่สำเร็จ',unicode(this_mail.get_receiver())+u' ปฏิเสธข้อเสนอการแลกเปลี่ยนของคุณ')
		sender=this_mail.get_sender()
		sender.money+=this_mail.money1
		sender.save()
		this_mail.transfer_items(1,sender)
		this_mail.delete()
		return JSONResponse({'success':True,'message':u'คุณได้ตอบปฏิเสธข้อเสนอนี้'})
	elif this_mail.type==5:
		if decliner=='receiver':
			send_alert(this_mail.get_sender(),u'การแลกเปลี่ยนไม่สำเร็จ',unicode(this_mail.get_receiver())+u' ปฏิเสธข้อเสนอการแลกเปลี่ยนของคุณ')
		else:
			send_alert(this_mail.get_receiver(),u'การแลกเปลี่ยนไม่สำเร็จ',unicode(this_mail.get_sender())+u' ปฏิเสธข้อเสนอการแลกเปลี่ยนของคุณ')
		
		receiver=this_mail.get_receiver()
		receiver.money+=this_mail.money1
		receiver.save()
		sender=this_mail.get_sender()
		sender.money+=this_mail.money2
		sender.save()
		this_mail.transfer_items(1,receiver)
		this_mail.transfer_items(2,sender)
		this_mail.delete()
		return JSONResponse({'success':True,'message':u'คุณได้ตอบปฏิเสธข้อเสนอนี้'})
	else:
		return JSONResponse({'success':False,'message':u'คุณไม่สามารถตอบรับข้อความนี้ได้'})

def testlist(request):
	x=request.POST.getlist('a')
	# print request.POST.getlist('a')
	return JSONResponse(x)

def testmail(request):
	return render_to_response('testpost.html')
