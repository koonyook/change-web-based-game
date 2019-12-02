# -*- coding: UTF-8 -*-
# Create your views here.
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from newtype.helpers.decorators import post_or_redirect_to_front
from newtype.helpers.http import JSONResponse
from newtype.core.models import Ownership,Union
from newtype.helpers.person import get_person_request , get_person_raw
from newtype.helpers.trim_time import trim_time
from newtype.core_union.models import Forum, Reply, SettingUnion

import math

OPEN_UNION_COST=1000000

#Forum part

#@post_or_redirect_to_front
def show_topic(request):
	all_forum = request.user.player.union.forum_set.all()
	data=list()
	for e in all_forum:
		data.append({
			'topic_id'		:e.id,
			'subject'		:e.subject,
			'owner'			:str(e.player),
			'last_reply_at'	:trim_time(e.reply_set.all().aggregate(Max('reply_at'))['reply_at__max']),
			'count_reply'	:e.reply_set.count()-1
		})
	return JSONResponse(data)

@post_or_redirect_to_front
def read_topic(request):
	topic_id=request.POST.get('topic_id','')
	try:
		this_topic=Forum.objects.get(id=topic_id)
	except ObjectDoesNotExist:
		return JSONResponse({'error_message':u'ขออภัย ไม่พบหัวข้อนี้'})
	if request.user.player.union!=this_topic.union:
		return JSONResponse({'error_message':u'ขออภัย นี้ไม่ใช้หัวข้อของบริษัทของคุณ'})
	data={
		'error_message'	:'',
		'subject'		:this_topic.subject
	}
	data['reply_list']=[]
	all_reply=this_topic.reply_set.all()
	for e in all_reply:
		data['reply_list'].append({
			'player_name'	:str(e.player),
			'reply_at'		:trim_time(e.reply_at),
			'message'		:e.message.replace('\n','<br/>')
		})
	return JSONResponse(data)

@post_or_redirect_to_front
def new_topic(request):
	subject=request.POST.get('subject','')
	message=request.POST.get('message','')
	if subject=='':
		return JSONResponse({'success':False,'message':u'คุณควรตั้งชื่อหัวข้อด้วย'})
	this_topic = Forum.objects.create(subject=subject,player=request.user.player,union=request.user.player.union)
	Reply.objects.create(forum=this_topic,player=request.user.player,message=message)
	return JSONResponse({'success':True,'message':u'หัวข้อใหม่ได้ถูกตั้งแล้ว'})

@post_or_redirect_to_front
def reply_topic(request):
	topic_id=request.POST.get('topic_id','')
	message=request.POST.get('message','')
	try:
		this_topic=Forum.objects.get(id=topic_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบหัวข้อนี้'})
	if request.user.player.union!=this_topic.union:
		return JSONResponse({'success':False,'message':u'ขออภัย นี้ไม่ใช้หัวข้อของบริษัทของคุณ'})
	Reply.objects.create(forum=this_topic,player=request.user.player,message=message)
	return JSONResponse({'success':True,'message':u'การตอบรับเสร็จสิ้น'})

@post_or_redirect_to_front
def delete_topic(request):
	topic_id=request.POST.get('topic_id','')
	try:
		this_topic=Forum.objects.get(id=topic_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบหัวข้อนี้'})
	if request.user.player.union!=this_topic.union:
		return JSONResponse({'success':False,'message':u'ขออภัย นี้ไม่ใช้หัวข้อของบริษัทของคุณ'})
	this_topic.delete()
	return JSONResponse({'success':True,'message':u'การลบหัวข้อเสร็จสิ้น'})

#Setting Part
#@post_or_redirect_to_front
def show_setting(request):
	data=dict()
	if request.user.player.union==None :
		return JSONResponse({'error_message':u'ขออภัย คุณยังไม่มีบริษัท'})
	else:
		data['error_message']=''

	if request.user.player.settingunion.can_set or (request.user.player.settingunion.rank==1):
		data['enable_setting']=True
	else:
		data['enable_setting']=False
	
	data['auto_share']=request.user.player.union.auto_share
	data['setting']=list()
	queryset=SettingUnion.objects.filter(player__union=request.user.player.union)
	for e in queryset:
		delete_button=False
		if e.rank!=1 :
			if (request.user.player.settingunion.rank==1) or (request.user.player.settingunion.can_set) or (e==request.user.player):
				delete_button=True
		data['setting'].append({
			'setting_id':e.id,
			'name':str(e.player),
			'can_research':e.can_research,
			'can_transfer_item':e.can_transfer_item,
			'can_take_money':e.can_take_money,
			'can_persuade':e.can_persuade,
			'can_set':e.can_set,
			'share_rate':e.share_rate,
			'delete_button':delete_button
		})
	return JSONResponse(data)

def to_bool(s):
	if(s==u'true'):
		return True
	else:
		return False

@post_or_redirect_to_front
def set_setting(request):
	auto_share		=request.POST.get('autoshare',False)
	id_list			=request.POST.getlist('id_list')
	can_research	=request.POST.getlist('can_research')
	can_transfer_item	=request.POST.getlist('can_transfer_item')
	can_take_money	=request.POST.getlist('can_take_money')
	can_persuade	=request.POST.getlist('can_persuade')
	can_set			=request.POST.getlist('can_set')
	share_rate		=request.POST.getlist('share_rate')
	print id_list
	print can_research
	print can_transfer_item
	#check condition
	if request.user.player.union==None :
		return JSONResponse({'success':False,'message':u'ขออภัย คุณยังไม่มีบริษัท'})
	if (not request.user.player.settingunion.can_set) and (request.user.player.settingunion.rank!=1):
		return JSONResponse({'success':False,'message':u'คุณไม่ได้รับอนุญาติให้วางแผนจัดการบุคคลในบริษัท'})

	#sum of share rate <= 100
	sum_rate=0
	for i in range(len(id_list)):
		try:
			SettingUnion.objects.get(id=id_list[i])
		except ObjectDoesNotExist:
			return JSONResponse({'success':False,'message':u'Some of id not found'})
		if auto_share:
			share_rate[i]='0'
		if share_rate[i]=='':
			share_rate[i]='0'
		if not share_rate[i].isdigit():
			return JSONResponse({'success':False,'message':u'ข้อมูลการปันผลผิดพลาดบางส่วน กรุณากรอกใหม่'})
		sum_rate+=int(share_rate[i])
	if sum_rate>100:
		return JSONResponse({'success':False,'message':u'ผลรวมของการปันผลทั้งหมดรวมกันห้ามเกิน 100%'})
	
	#pass all condition then setting
	request.user.player.union.auto_share=to_bool(auto_share)
	request.user.player.union.save()
	for i in range(len(id_list)):
		this_set=SettingUnion.objects.get(id=id_list[i])
		this_set.can_research=to_bool(can_research[i])
		this_set.can_transfer_item=to_bool(can_transfer_item[i])
		this_set.can_take_money=to_bool(can_take_money[i])
		this_set.can_persuade=to_bool(can_persuade[i])
		this_set.can_set=to_bool(can_set[i])
		if not auto_share:
			this_set.share_rate=int(share_rate[i])
		this_set.save()
	return JSONResponse({'success':True,'message':u'การเปลี่ยนแปลงค่า เสร็จสิ้น'})

@post_or_redirect_to_front
def delete_member(request):
	set_id =request.POST.get('setting_id','')
	try:
		this_set=SettingUnion.objects.get(id=set_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ไม่พบสมาชิกผู้นี้'})
	this_set.player.union=None
	this_set.player.save()
	this_set.can_research=False
	this_set.can_transfer_item=False
	this_set.can_take_money=False
	this_set.can_persuade=False
	this_set.can_set=False
	this_set.share_rate=0
	this_set.union_rank=None
	this_set.save()
	return JSONResponse({'success':True,'message':u'พนักงาน '+str(this_set.player)+u' ได้ออกไปจากบริษัทนี้แล้ว'})

#Transfer path
CANNOT_DEAL_TYPE = set([u'เทคโนโลยี',u'ขยะ'])
#@post_or_redirect_to_front
def transfer_item(request):
	item_id = request.POST.get('item_id','')
	try:
		this_item=Ownership.objects.get(id=item_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบไอเทมนี้ใน server'})
	
	if request.user.player.union==None:
		return JSONResponse({'success':False,'message':u'คุณยังไม่มีบริษัท'})
	
	if get_person_request(request)!=this_item.get_owner():
		return JSONResponse({'success':False,'message':u'คุณไม่สามารถโอนย้ายไอเทมของผู้อื่นได้'})
	
	if not request.user.player.settingunion.can_transfer_item : 
		return JSONResponse({'success':False,'message':u'คุณไม่ได้รับอณุญาตให้โอนย้ายไอเทมระหว่างคุณกับบริษัท'})

	if len( set(this_item.item.get_item_types_list()) & CANNOT_DEAL_TYPE )>0 :
		return JSONResponse({'success':False,'message':u'คุณไม่สามารถโอนย้ายเทคโนโลยีได้'})

	if this_item.is_available==False:
		return JSONResponse({'success':False,'message':u'ไอเทมของคุณถูกนำไปใช้อยู่'})

	if request.session['state']=='player':
		if request.user.player.union.get_free_space()<this_item.item.storage_cost:
			return JSONResponse({'success':False,'message':u'บริษัทของคุณเหลือที่ไม่พอจะเก็บไอเทมนี้'})
		this_item.set_owner(request.user.player.union)
	elif request.session['state']=='union':
		if request.user.player.get_free_space()<this_item.item.storage_cost:
			return JSONResponse({'success':False,'message':u'ตัวคุณเหลือที่ไม่พอสำหรับไอเทมนี้'})
		this_item.set_owner(request.user.player)
	return JSONResponse({'success':True,'message':u'การโอนย้ายไอเทมเสร็จสิ้น'})

#@post_or_redirect_to_front
def transfer_money(request):
	money = request.POST.get('money','')
	if not money.isdigit():
		return JSONResponse({'success':False,'message':u'จำนวนเงินผิดพลาด กรุณากรอกใหม่'})

	money=int(money)
	if request.user.player.union==None:
		return JSONResponse({'success':False,'message':u'คุณยังไม่มีบริษัท'})
	
	if request.session['state']=='player':
		if money>request.user.player.money:
			return JSONResponse({'success':False,'message':u'คุณมีเงินไม่พอ'})
		request.user.player.money-=money
		request.user.player.union.money+=money
	elif request.session['state']=='union':
		if not request.user.player.settingunion.can_take_money :
			return JSONResponse({'success':False,'message':u'คุณไม่ได้รับอนุญาตให้โอนเงินจากบริษัท'})
		if money>request.user.player.union.money:
			return JSONResponse({'success':False,'message':u'บริษัทมีเงินไม่พอ'})
		request.user.player.money+=money
		request.user.player.union.money-=money
	request.user.player.save()
	request.user.player.union.save()

	return JSONResponse({'success':True,'message':u'การโอนเงินเสร็จสมบูรณ์'})

#union cannot delete now (don't care)

def get_open_cost(request):
	return JSONResponse(unicode(OPEN_UNION_COST))

def new_union(request):
	union_name = request.POST.get('union_name')
	try:
		Union.objects.get(name=union_name)
		return JSONResponse({'success':False,'message':u'ชื่อบริษัท '+union_name+u' ได้ถูกจดทะเบียนไว้แล้ว'})
	except ObjectDoesNotExist:
		pass

	head=request.user.player
	if head.union!=None:
		return JSONResponse({'success':False,'message':u'คุณมีบริษัทอยู่แล้ว'})
	if head.money<OPEN_UNION_COST:
		return JSONResponse({'success':False,'message':u'การจดทะเบียนบริษัทต้องใช้เงินเป็นจำนวน $'+str(OPEN_UNION_COST)})

	union=Union.objects.create(name=union_name,storage=500,energy=5000,max_energy=5000,mechanical_energy=5000,max_mechanical_energy=5000,research_cost=80,regeneration_rate=60)

	head.settingunion.can_research			= True
	head.settingunion.can_transfer_item		= True
	head.settingunion.can_take_money		= True
	head.settingunion.can_persuade			= True
	head.settingunion.can_set				= True
	head.settingunion.rank					= 1
	head.settingunion.save()

	head.union=union
	head.money-=OPEN_UNION_COST
	head.save()
	return JSONResponse({'success':True,'message':u'ขณะนี้ คุณได้เป็นประธานบริษัทของบริษัท "'+union_name+'".'+u' คุณสามารถส่งจดหมายเชิญผู้เล่นอื่นๆ เข้าบริษัทได้'})

#this method may be call from income of patent
def share_income(union,money):
	queryset=union.player_set.all()
	
	if union.auto_share:
		num=queryset.count()
		money_get=floor(money/num)
		for e in queryset:
			e.money+=money_get
			e.save()
		union.money+=money-(money_get*num)
		union.save()
	else:
		money_sum=0
		for e in queryset:
			money_get=floor(money*e.settingunion.share_rate/100.0)
			e.money+=money_get
			e.save()
			money_sum+=money_get
		union.money-=money-money_sum
		union.save()