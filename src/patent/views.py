# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from newtype.helpers.http import JSONResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from newtype.helpers.decorators import post_or_redirect_to_front

from django.core.exceptions import ObjectDoesNotExist

from newtype.core.models import Ownership,Item,Player,Union,ResearchLog,ServerStatus
from newtype.mail.views import send_alert
from newtype.patent.models import Patent

from newtype.helpers.person import get_person_request , get_person_raw
from newtype.helpers.trim_time import trim_time
import datetime
import math

# Create your views here.
def show_all_patent(request):
	patent_enabled=bool(int(ServerStatus.objects.get(name='patent_enabled').value))
	data=list()
	if not patent_enabled:
		queryset=Patent.objects.exclude(founder=None)
		queryset=queryset.order_by('-found_at')
		tmp=queryset.select_related(depth=3)
		for e in tmp:
			data.append({
				'id'		:e.id,
				'name'		:e.formula.name,
				'found_at'	:trim_time(e.found_at),
				'founder'	:unicode(e.founder)
			})
		return JSONResponse({'can_click':False ,'data':data})		#this cannot click to read patent
	
	queryset=Patent.objects.filter(status__in=[1,2])
	queryset=queryset.order_by('-found_at')
	tmp=queryset.select_related(depth=3)
	for e in tmp:
		data.append({
			'id'		:e.id,
			'name'		:e.formula.name,
			'found_at'	:trim_time(e.found_at),
			'founder'	:unicode(e.founder)
		})
	return JSONResponse({'can_click':True ,'data':data})			#this can click to read patent

#@post_or_redirect_to_front
def show_person_patent(request):	
	person = get_person_request(request)
	queryset=Patent.objects.filter(status__in=[1])
	queryset=queryset.order_by('-regis_at')
	tmp=queryset.select_related(depth=3)
	data=list()
	for e in tmp:
		if e.get_owner()==person:
			data.append({
				'id'		:e.id,
				'name'		:e.formula.name,
				'regis_at'	:trim_time(e.regis_at)
			})
	return JSONResponse(data)

@post_or_redirect_to_front
def read_patent(request):
	patent_id = request.POST.get('patent_id','')
	person = get_person_request(request)
	try:
		queryset=Patent.objects.filter(status__in=[0,1,2])
		this_patent=queryset.get(id=patent_id)
	except ObjectDoesNotExist:
		return JSONResponse({'error_message':u'ขออภัย ไม่พบสิทธิบัตรนี้ใน server'})
	data={
		'error_message':'',
		'id'		:this_patent.id,
		'status'	:this_patent.status,
		'status_name':this_patent.get_status_display(),
		'owner'		:unicode(this_patent.get_owner()),
		'regis_at'	:trim_time(this_patent.regis_at),
		'regis_cost':this_patent.regis_cost,
		'copy_cost'	:this_patent.copy_cost,

		'name'		:this_patent.formula.name,
		'description':this_patent.formula.description,
		'weather'	:unicode(this_patent.formula.weather)
	}
	comp=[]
	tmp=this_patent.formula.components.all()
	for e in tmp:
		comp.append(e.name)
	tmp=this_patent.formula.component_types.all()
	for e in tmp:
		comp.append('Type:'+e.name)
	data['component']=comp

	res=[]
	tmp=this_patent.formula.results.all()
	for e in tmp:
		res.append(e.name)
	data['result']=res

	if this_patent.get_owner()==person and this_patent.is_available==True:
		data['give_button']=True			#Show two button 1.Give to the world 2.Give to some one
	else:
		data['give_button']=False			#Show information only
	
	return JSONResponse(data)

@post_or_redirect_to_front
def open_patent(request):					#not secure
	patent_id = request.POST.get('patent_id','')

	try:
		queryset=Patent.objects.filter(status__in=[1,2])
		this_patent=queryset.get(id=patent_id)
	except ObjectDoesNotExist:
		return JSONResponse(u'ขออภัย ไม่พบสิทธิบัตรนี้ใน server')
	
	if not this_patent.is_available :
		return JSONResponse(u'สิทธิบัตรของคุณถูกตั้งขายอยู่ กรุณายกเลิกการตั้งขายก่อน')

	this_patent.status=2
	this_patent.player=None
	this_patent.union=None
	this_patent.save()
	return JSONResponse(u'โลกคงอยากที่จะขอบคุณในความแสนดีของคุณ')

@post_or_redirect_to_front
def give_patent(request):					#not secure
	patent_id = request.POST.get('patent_id','')
	send_to = request.POST.get('send_to','')			#'player' or 'union'
	target_name = request.POST.get('target_name','')

	try:
		queryset=Patent.objects.filter(status__in=[1])
		this_patent=queryset.get(id=patent_id)
	except ObjectDoesNotExist:
		return JSONResponse(u'ขออภัย ไม่พบสิทธิบัตรนี้ใน server')
	person=get_person_raw(send_to,target_name)
	if person==None :
		return JSONResponse(u'ขออภัย ไม่พบชื่อของบุคคลที่คุณกรอก')
	if not this_patent.is_available :
		return JSONResponse(u'สิทธิบัตรของคุณถูกตั้งขายอยู่ กรุณายกเลิกการตั้งขายก่อน')
	owner=this_patent.get_owner()
	this_patent.set_owner(person)
	this_patent.save()
	send_alert(person,u'คุณได้รับสิทธิบัตรจาก...',unicode(owner)+u' ได้มอบสิทธิบัตร '+this_patent.formula.name+u' ให้กับคุณ')
	return JSONResponse(u'สิทธิบัตรได้ถูกโอนกรรมสิทธิไปเป็นของ '+unicode(person)+u'เรียบร้อยแล้ว')

@post_or_redirect_to_front
def regis_patent(request):
	regis_type = request.POST.get('regis_type','')		#'regis' or 'open'
	patent_id = request.POST.get('patent_id','')
	person = get_person_request(request)
	try:
		queryset=Patent.objects.filter(status__in=[0])
		this_patent=queryset.get(id=patent_id)
	except ObjectDoesNotExist:
		return JSONResponse(u'คุณช้าเกินไป มีผู้จดสิทธิบัตรนี้ไปแล้ว')
	
	if this_patent.regis_cost==None :
		return JSONResponse(u'ขออภัย สิทธิบัตรนี้ถูกสงวนไว้ ไม่สารมารจดสิทธิบัตรได้')

	if type(person)==Player:
		success_log=ResearchLog.objects.filter(player=person, is_success=True, formula=this_patent.formula)
	else:
		success_log=ResearchLog.objects.filter(union=person, is_success=True, formula=this_patent.formula)
	
	if success_log==ResearchLog.objects.none() :
		return JSONResponse(u'ขออภัย คุณต้องเคยวิจัยสิ่งนี้สำเร็จมาแล้วอย่างน้อยหนึ่งครั้ง')
	
	#pass all condition
	if regis_type=='regis':
		if person.money < this_patent.regis_cost:
			return JSONResponse(u'ขออภัย คุณมีเงินไม่พอจ่ายค่าธรรมเนียมการจดสิทธิบัตร($'+unicode(this_patent.regis_cost)+')')
		person.money-=this_patent.regis_cost
		person.save()
		this_patent.status=1
		this_patent.set_owner(person)
		this_patent.regis_at=datetime.datetime.now()
		this_patent.save()
		return JSONResponse(u'ยินดีด้วย สิทธิบัตรเป็นของคุณแล้ว')
	elif regis_type=='open': 
		this_patent.status=2
		this_patent.regis_at=datetime.datetime.now()
		this_patent.save()
		return JSONResponse(u'โลกคงอยากที่จะขอบคุณในความแสนดีของคุณ')
	
	return JSONResponse(u'Sorry, regis_type invalid')