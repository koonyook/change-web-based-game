# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from newtype.helpers.http import JSONResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from newtype.helpers.decorators import post_or_redirect_to_front
from newtype.patent.models import Patent

from django.core.exceptions import ObjectDoesNotExist

from newtype.core.models import Ownership,Item,Union,Player,ServerStatus
from newtype.market.models import Sell, Buy ,SellPatent

from newtype.helpers.person import get_person_request , get_person_raw
from newtype.helpers.trim_time import trim_time

import datetime
import math

CANNOT_DEAL_TYPE = set([u'เทคโนโลยี',u'ขยะ'])
#TAX_RATE = 0.01		#tax 1%
EXPIRE_TIME=datetime.timedelta(days=3)
# Create your views here.
def cmp_price_L_to_H(data1,data2): return int(data1['price']-data2['price'])   
def cmp_price_H_to_L(data1,data2): return int(data2['price']-data1['price'])

def cmp_level_L_to_H(data1,data2): return int(data1['level']-data2['level'])
def cmp_level_H_to_L(data1,data2): return int(data2['level']-data1['level'])

def cmp_item_name(data1,data2): return cmp(data1['item_name'],data2['item_name'])

@post_or_redirect_to_front
def search_in_sell(request):
	item_name = request.POST.get('item_name','')
	level = request.POST.get('level','')
	sort_by = request.POST.get('sort_by','price')			#'price' or 'level'
	
	person=get_person_request(request)
	queryset = Sell.objects.all()
	expire_set = queryset.filter(expire_at__lt=datetime.datetime.now())
	for e in expire_set:
		e.cancle()

	if item_name!='':
		queryset = queryset.filter(item__item__name__contains=item_name)
	if level.isdigit() :
		queryset = queryset.filter(item__level=int(level))
	temp=queryset.select_related(depth=4)	#for do not hit database again
	data=list()
	for e in temp:
		if (e.item.get_owner()==person):
			cancle_button=True
		else:
			cancle_button=False
		data.append({
			'id'		:e.id,
			'price'		:e.price,
			'expire_at'	:trim_time(e.expire_at),
			'level'		:e.item.level,
			'durability':e.item.durability,
			'item_name'	:e.item.item.name,
			'icon_url'	:e.item.item.get_full_icon_url(),
			'max_durability':e.item.item.durability,
			'storage_cost':e.item.item.storage_cost,
			'seller'	:unicode(e.item.get_owner()),
			'cancle_button':cancle_button
		})
		
	if sort_by == 'level':
		data.sort(cmp_price_L_to_H)
		data.sort(cmp_level_H_to_L)
	else:
		data.sort(cmp_level_H_to_L)
		data.sort(cmp_price_L_to_H)
	data.sort(cmp_item_name)	

	return JSONResponse(data)

@post_or_redirect_to_front
def search_in_buy(request):
	view_by	= request.session['state']
	
	item_name = request.POST.get('item_name','')
	level = request.POST.get('level','')				# this is ceiling level (system will search buy lists that have level<=ceiling level)
	can_sell = request.POST.get('can_sell','False')			# 'True' or 'False'  (only filter item, do not filter level 
	sort_by = request.POST.get('sort_by','price')			# 'price' or 'level'
	
	queryset = Buy.objects.all()
	
	expire_set = queryset.filter(expire_at__lt=datetime.datetime.now())
	for e in expire_set:
		e.cancle()

	if item_name!='':
		queryset = queryset.filter(item__name__contains=item_name)
	if level.isdigit():
		queryset = queryset.filter(level__lte=int(level))  #Less than or equal to
	if can_sell=='True':
		if view_by=='player':
			owner = Ownership.objects.filter(player=request.user.player).values_list('item')
		else:
			owner = Ownership.objects.filter(union=request.user.player.union).values_list('item')
		queryset = queryset.filter(item__in=owner)
	temp=queryset.select_related(depth=3)	#for do not hit database again
	person=get_person_request(request)
	data=list()
	for e in temp:
		if (e.get_buyer()==person):
			cancle_button=True
		else:
			cancle_button=False
		data.append({
			'id'		:e.id,
			'price'		:e.price,
			'expire_at'	:trim_time(e.expire_at),
			'level'		:e.level,
			'item_name'	:e.item.name,
			'icon_url'	:e.item.get_full_icon_url(),
			'quantity'	:e.quantity,
			'buyer'		:unicode(e.get_buyer()),
			'must_complete':e.must_complete,
			'cancle_button':cancle_button
		})

	if sort_by == 'level':
		data.sort(cmp_price_H_to_L)
		data.sort(cmp_level_L_to_H)
	else:
		data.sort(cmp_level_L_to_H)
		data.sort(cmp_price_H_to_L)
	data.sort(cmp_item_name)	

	return JSONResponse(data)

@post_or_redirect_to_front
def new_sell(request):
	price = request.POST.get('price','')
	item_id = request.POST.get('item_id','')		#id of Ownership
	
	try:
		item=Ownership.objects.get(id=item_id)
	except ObjectDoesNotExist:
		return JSONResponse(u'ขออภัย ไม่พบไอเทมนี้ใน server')
	TAX_RATE=float(ServerStatus.objects.get(name='tax_rate').value)
	seller=item.get_owner()
	if type(seller)==Union:
		if not (request.user.player.settingunion.can_transfer_item and request.user.player.settingunion.can_take_money):
			return JSONResponse(u'ขออภัย คุณไม่ได้รับอณุญาตจากบริษัทให้ทำสิ่งนี้ (การโอนเงิน และ ไอเทม)')
	if (not price.isdigit()) or int(price)<=0 :
		return JSONResponse(u'ขออภัย ข้อมูลจำนวนเงินผิดพลาด กรุณากรอกใหม่')
	price=int(price)
	intersected=set(item.item.get_item_types_list()) & CANNOT_DEAL_TYPE
	if (len(intersected) >0) or (item.item.expiration!=None):
		return JSONResponse(u'ขออภัย ไอเทมนี้ไม่สามารถขายได้')
	if (item.is_available==False):
		return JSONResponse(u'ขออภัย ไอเทมของคุณอาจจะถูกตั้งขายอยู่แล้ว')
	if (seller.money<price*TAX_RATE):
		return JSONResponse(u'ขออภัย คุณมีเงินไม่พอสำหรับจ่ายภาษี (%s %%)' % (TAX_RATE * 100))
	#pass all condition then can sell
	item.is_available=False
	tax=math.ceil(price*TAX_RATE)
	seller.money-=tax
	newsell=Sell(item=item,price=price,expire_at=datetime.datetime.now()+EXPIRE_TIME)
	seller.save()
	item.save()
	newsell.save()
	return JSONResponse(u'การตั้งขายเสร็จสิ้น คุณเสียภาษีเป็นจำนวนเงิน $'+unicode(tax))

#@post_or_redirect_to_front
def can_buy(request):						# "skip" don't care union buying that can buy only a member known item 
	#print request.user.player.known_items.all()
	data=list(request.user.player.known_items.all().values('id','name'))
	return JSONResponse(data)

@post_or_redirect_to_front
def new_buy(request):	
	price = request.POST.get('price','')			#full price
	item_id = request.POST.get('item_id','')		#id of item(Not Ownership)
	level = request.POST.get('level','')
	quantity = request.POST.get('quantity','')
	must_complete=request.POST.get('must_complete','') #'True' or 'False'
	
	try:
		item=Item.objects.get(id=item_id)
	except ObjectDoesNotExist:
		return JSONResponse(u'ขออภัย ไม่พบไอเทมนี้ใน server')
	TAX_RATE=float(ServerStatus.objects.get(name='tax_rate').value)
	person=get_person_request(request)
	if type(person)==Union:
		if not (request.user.player.settingunion.can_transfer_item and request.user.player.settingunion.can_take_money):
			return JSONResponse(u'ขออภัย คุณไม่ได้รับอณุญาตจากบริษัทให้ทำสิ่งนี้ (การโอนเงิน และ ไอเทม)')

	if (not price.isdigit()) or int(price)<=0 :
		return JSONResponse(u'ขออภัย ข้อมูลจำนวนเงินผิดพลาด กรุณากรอกใหม่')
	price=int(price)
	if (not level.isdigit()) or int(level)<=0 :
		return JSONResponse(u'ขออภัย ข้อมูล level ผิดพลาด กรุณากรอกใหม่')
	level=int(level)
	if (not quantity.isdigit()) or int(quantity)<=0 :
		return JSONResponse(u'ขออภัย ข้อมูลจำนวนรับซื้อผิดพลาด กรุณากรอกใหม่')
	quantity=int(quantity)
	if (person.get_free_space()<item.storage_cost*quantity ):
		return JSONResponse(u'ขออภัย คุณมีพื้นที่ไม่พอที่จะจองไว้สำหรับการรับซื้อไอเทมทั้งหมด')
	if (person.money< price*quantity*(1+TAX_RATE) ):
		return JSONResponse(u'ขออภัย คุณมีเงินไม่พอสำหรับจ่ายภาษี(%s %%).' % (TAX_RATE * 100))
	#pass all condition then can buy
	if must_complete=='True': must_complete=True
	else : must_complete=False
	cost=price*quantity
	tax=math.ceil(price*quantity*TAX_RATE)
	person.money-=(cost+tax)
	person.reserve_space+=(item.storage_cost*quantity)
	newbuy=Buy(item=item,price=price,expire_at=datetime.datetime.now()+EXPIRE_TIME,level=level,quantity=quantity,must_complete=must_complete)
	newbuy.set_buyer(person)
	person.save()
	newbuy.save()
	return JSONResponse(u'การตั้งรับซื้อเสร็จสิ้น คุณเสียเงินและภาษี $'+unicode(int(cost)))

@post_or_redirect_to_front
def player_buy(request):
	sell_id=request.POST.get('sell_id','')
	
	person=get_person_request(request)
	if type(person)==Union:
		if not (request.user.player.settingunion.can_transfer_item and request.user.player.settingunion.can_take_money):
			return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่ได้รับอณุญาตจากบริษัทให้ทำสิ่งนี้ (การโอนเงิน และ ไอเทม)'})
	try:
		this_sell=Sell.objects.get(id=sell_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบรายการขายนี้อยู่'})

	if this_sell.expire_at<datetime.datetime.now():
		this_sell.cancle()
		return JSONResponse({'success':False,'message':u'ขออภัย รายการขายนี้ได้หมดอายุไปแล้ว'})

	if (person.get_free_space()<this_sell.item.item.storage_cost ):
		return JSONResponse({'success':False,'message':u'คุณมีพื้นที่ไม่พอสำหรับซื้อไอเทมนี้'})
	if (person.money< this_sell.price ):
		return JSONResponse({'success':False,'message':u'คุณมีเงินที่ไม่พอสำหรับซื้อไอเทมนี้'})
	
	#pass all condition then player can buy
	seller=this_sell.item.get_owner()
	#transfer money
	cost=this_sell.price
	seller.money=seller.money+cost
	person.money-=cost

	seller.save()		#must save before transfer item
	#transfer item
	this_sell.item.set_owner(person)
	#unlock item
	this_sell.item.is_available=True
	#add known item
	person.known_items.add(this_sell.item.item)
	#save change and delete Sell
	
	person.save()
	this_sell.item.save()
	this_sell.delete()
	return JSONResponse({'success':True,'message':u'การซื้อเสร็จสิ้น คุณจ่าย $'+unicode(int(cost))})

#@post_or_redirect_to_front
def player_sell(request):
	buy_id=request.POST.get('buy_id','')
	item_id=request.POST.get('item_id','')
	
	try:
		this_buy=Buy.objects.get(id=buy_id)
		item=Ownership.objects.get(id=item_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบรายการขายหรือไอเทมของคุณ'})

	if type(item.get_owner())==Union:
		if not (request.user.player.settingunion.can_transfer_item and request.user.player.settingunion.can_take_money):
			return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่ได้รับอณุญาตจากบริษัทให้ทำสิ่งนี้ (การโอนเงิน และ ไอเทม)'})

	if this_buy.expire_at<datetime.datetime.now():
		this_buy.cancle()
		return JSONResponse({'success':False,'message':u'ขออภัย รายการรับซื้อนี้หมดอายุแล้ว'})
	if (not item.is_available):
		return JSONResponse({'success':False,'message':u'ไอเทมของคุณ อาจถูกตั้งขายอยู่ กรุณายกเลิกรายการตั้งขายไอเทมของคุณก่อน'})
	if (item.item != this_buy.item or item.level<this_buy.level):
		return JSONResponse({'success':False,'message':u'ขออภัย ไอเทมของคุณไม่ตรงตามความต้องการของผู้ซื้อ'})
	if this_buy.must_complete and item.durability!=item.item.durability :
		return JSONResponse({'success':False,'message':u'ขออภัย ไอเทมของคุณไม่สมบูรณ์ตามที่ผู้รับซื้อต้องการ'})

	#pass all condition then player can sell
	seller=item.get_owner()
	buyer=this_buy.get_buyer()
	
	#transfer money
	if item.durability!=None:
		cost_get=int(math.floor(this_buy.price*item.durability/item.item.durability))
	else:
		cost_get=this_buy.price
	buyer.money=buyer.money+this_buy.price-cost_get
	seller.money+=cost_get
	#transfer item
	item.set_owner(buyer)
	#unlock buyer space
	buyer.reserve_space-=this_buy.item.storage_cost
	#unlock item
	item.is_available=True
	#decrease quantity
	this_buy.quantity-=1
	#save and delete if quantity is zero
	buyer.save()
	seller.save()
	item.save()
	this_buy.save()

	if this_buy.quantity==0 :
		this_buy.delete()

	return JSONResponse({'success':True,'message':u'การขายสำเร็จ คุณได้รับเงิน $'+unicode(int(cost_get))})
	
@post_or_redirect_to_front
def cancel_sell(request):
	sell_id=request.POST.get('sell_id','')
	
	try:
		this_sell=Sell.objects.get(id=sell_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบรายการขายนี้ใน server'})

	if this_sell.item.get_owner()!=get_person_request(request) :
		return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่สามารถยกเลิกการขายของผู้อื่นได้'})

	this_sell.cancle()
	return JSONResponse({'success':True,'message':u'คุณได้ยกเลิกการขายเรียบร้อยแล้ว'})

@post_or_redirect_to_front
def cancel_buy(request):
	buy_id=request.POST.get('buy_id','')
	
	try:
		this_buy=Buy.objects.get(id=buy_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบรายการรับซื้อนี้ใน server'})

	if this_buy.get_buyer()!=get_person_request(request) :
		return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่สามารถยกเลิกการรับซื้อของผู้อื่นได้'})
	get_back=this_buy.cancle()
	return JSONResponse({'success':True,'message':u'คุณได้ยกเลิกการรับซื้อเรียบร้อยแล้ว, คุณได้รับพื้นที่ และได้รับเงินคืนเป็นจำนวน $'+unicode(int(get_back))})

@post_or_redirect_to_front
def sell_bank(request):
	'''rabob rub zie'''
	item_id=request.POST.get('item_id','')
	
	person=get_person_request(request)
	if type(person)==Union:
		if not (request.user.player.settingunion.can_transfer_item and request.user.player.settingunion.can_take_money):
			return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่ได้รับอณุญาตจากบริษัทให้ทำสิ่งนี้ (การโอนเงิน และ ไอเทม)'})
	try:
		item=Ownership.objects.get(id=item_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบไอเทมนี้ใน server'})

	if (item.item.price==None):
		return JSONResponse({'success':False,'message':u'ขออภัย ไอเทมนี้ไม่สามารถขายได้'})
	if (not item.is_available):
		return JSONResponse({'success':False,'message':u'ขออภัย ไอเทมของคุณอาจจะถูกตั้งขายอยู่แล้ว กรุณายกเลิกรายการตั้งขายก่อน'})
	if item.get_owner()!=person:
		return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่สามารถตั้งขายไอเทมของผู้อื่นได้'})
	#pass all condition
	if item.durability!=None:
		money_get=int(math.floor(item.item.price*item.durability/item.item.durability))
	else:
		money_get=this_buy.price
	person.money+=money_get
	item.delete()
	person.save()
	return JSONResponse({'success':True,'message':u'การขายเสร็จสิ้น คุณได้เงิน $'+unicode(money_get)})

#@post_or_redirect_to_front
def show_sell_patent(request):
	person=get_person_request(request)
	queryset=SellPatent.objects.all()
	queryset=queryset.order_by('-start_at')
	tmp=queryset.select_related(depth=3)
	data=list()
	for e in tmp:
		if (e.patent.get_owner()==person):
			cancle_button=True
		else:
			cancle_button=False
		data.append({
			'sell_id'	:e.id,								# use with buy_patent
			'patent_id'	:e.patent.id,						# use with read_patent to show detail
			'price'		:e.price,
			'name'		:e.patent.formula.name,
			'seller'	:unicode(e.patent.get_owner()),
			'cancle_button':cancle_button
		})
	return JSONResponse(data)

#@post_or_redirect_to_front
def can_sell_patent(request):
	sell_by=request.session['state']
	person=get_person_request(request)
	if sell_by=='player':
		queryset=Patent.objects.filter(player=person)
	else:
		queryset=Patent.objects.filter(union=person)
	
	queryset=queryset.filter(status__in=[1])
	tmp=queryset.select_related(depth=3)
	data=list()
	for e in tmp:
		data.append({
			'patent_id'	:e.id,						
			'name'		:e.formula.name
		})
	return JSONResponse(data)

@post_or_redirect_to_front
def new_sell_patent(request):
	price = request.POST.get('price','')
	patent_id = request.POST.get('patent_id','')		#id of Ownership
	
	try:
		queryset=Patent.objects.filter(status__in=[1])
		patent=queryset.get(id=patent_id)
	except ObjectDoesNotExist:
		return JSONResponse(u'ขออภัย ไม่พบสิทธิบัตรนี้ใน server')
	TAX_RATE=float(ServerStatus.objects.get(name='tax_rate').value)
	seller=patent.get_owner()
	if type(seller)==Union:
		if not (request.user.player.settingunion.can_transfer_item and request.user.player.settingunion.can_take_money):
			return JSONResponse(u'ขออภัย คุณไม่ได้รับอณุญาตจากบริษัทให้ทำสิ่งนี้ (การโอนเงิน และ ไอเทม)')
	if (not price.isdigit()) or int(price)<=0 :
		return JSONResponse(u'ขออภัย ข้อมูลจำนวนเงินผิดพลาด กรุณากรอกใหม่')
	price=int(price)
	if (patent.is_available==False):
		return JSONResponse(u'ขออภัย สิทธิบัตรของคุณอาจจะถูกตั้งขายอยู่แล้ว')
	if (seller.money<price*TAX_RATE):
		return JSONResponse(u'ขออภัย คุณมีเงินไม่พอสำหรับจ่ายภาษี (%s %%)' % (TAX_RATE * 100))
	#pass all condition then can sell
	patent.is_available=False
	tax=math.ceil(price*TAX_RATE)
	seller.money-=tax
	newsell=SellPatent(patent=patent,price=price)
	seller.save()
	patent.save()
	newsell.save()
	return JSONResponse(u'การตั้งขายสิทธิบัตรเสร็จสิ้น คุณเสียภาษีเป็นจำนวนเงิน $'+unicode(tax))

#@post_or_redirect_to_front
def buy_patent(request):
	sell_id=request.POST.get('sell_patent_id','')
	
	buyer=get_person_request(request)
	if type(buyer)==Union:
		if not (request.user.player.settingunion.can_transfer_item and request.user.player.settingunion.can_take_money):
			return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่ได้รับอณุญาตจากบริษัทให้ทำสิ่งนี้ (การโอนเงิน และ ไอเทม)'})
	try:
		this_sell=SellPatent.objects.get(id=sell_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบรายการขายนี้ใน server'})

	if (buyer.money < this_sell.price ):
		return JSONResponse({'success':False,'message':u'ขออภัย คุณมีเงินไม่เพียงพอ'})
	
	#pass all condition then player can buy
	seller=this_sell.patent.get_owner()
	#transfer money
	cost=this_sell.price
	seller.money+=cost
	buyer.money-=cost

	seller.save()		#must save before transfer item
	#transfer item
	this_sell.patent.set_owner(buyer)
	#unlock item
	this_sell.patent.is_available=True

	#save change and delete Sell	
	buyer.save()
	this_sell.patent.save()
	this_sell.delete()
	return JSONResponse({'success':True,'message':u'การซื้อสิทธิบัตรเสร็จสิ้น คุณจ่ายเงิน $'+unicode(int(cost))})

#@post_or_redirect_to_front
def cancel_sell_patent(request):
	sell_patent_id=request.POST.get('sell_patent_id','')
	
	try:
		this_sell=SellPatent.objects.get(id=sell_patent_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบรายการขายนี้ใน server'})

	if this_sell.patent.get_owner()!=get_person_request(request) :
		return JSONResponse({'success':False,'message':u'ขออภัย คุณไม่สามารถยกเลิกการตั้งขายสิทธิบัตรของผู้อื่นได้'})

	this_sell.cancle()
	return JSONResponse({'success':True,'message':u'คุณได้ยกเลิกการขายนี้แล้ว'})

def dbug(request):
	return render_to_response('markettest.html')
