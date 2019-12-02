# -*- coding: UTF-8 -*-
# Create your views here.
from newtype.helpers.decorators import post_or_redirect_to_front
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from newtype.helpers.http import JSONResponse
from newtype.core.models import ServerStatus,Formula,Ownership
from newtype.help.models import QuestionAnswer
from django.core.exceptions import ObjectDoesNotExist
from random import randint

#@post_or_redirect_to_front
def get_enabled_menu(request):
	data={}
	data['story']={'name':u'เนื้อเรื่อง','tag':u'story'}		
	data['research']={'name':u'การวิจัย','tag':u'research'}
	data['yourstatus']={'name':u'สถานะของคุณ','tag':u'yourstatus'}
	data['item']={'name':u'ไอเทม และ ทรัพยากร','tag':u'item'}		# item and natural resource
	data['patent']={'name':u'สิทธิบัตร','tag':u'patent'}
	data['mailbox']={'name':u'กล่องจดหมาย','tag':u'mailbox'}
	data['economy']={'name':u'เศรษฐกิจ','tag':u'economy'}
	data['union']={'name':u'บริษัท','tag':u'union'}
	data['disaster']={'name':u'ภัยธรรมชาติ','tag':u'disaster'}
	data['worldstatus']={'name':u'สถานะของโลก','tag':u'worldstatus'}
	data['trick']={'name':u'เคล็ดลับ','tag':u'trick'}
	data['qanda']={'name':u'คำถามที่พบบ่อย','tag':u'qanda'}		# Q&A

	data['story']['enabled']=True	
	data['research']['enabled']=True
	data['yourstatus']['enabled']=True
	data['item']['enabled']=True		# item and natural resource
	data['patent']['enabled']=False
	data['mailbox']['enabled']=True
	data['economy']['enabled']=False
	data['union']['enabled']=False
	data['disaster']['enabled']=True
	data['worldstatus']['enabled']=True
	data['trick']['enabled']=True
	data['qanda']['enabled']=True		# Q&A

	if ServerStatus.objects.get(name='patent_enabled').value=='1':
		data['patent']['enabled']=True

	if ServerStatus.objects.get(name='market_enabled').value=='1' or ServerStatus.objects.get(name='bank_enabled').value=='1' or ServerStatus.objects.get(name='patent_enabled').value=='1':
		data['economy']['enabled']=True

	if ServerStatus.objects.get(name='union_enabled').value=='1':
		data['union']['enabled']=True

	l=list()
	l.append(data['story'])
	l.append(data['research'])
	l.append(data['yourstatus'])
	l.append(data['item'])
	l.append(data['patent'])
	l.append(data['mailbox'])
	l.append(data['economy'])
	l.append(data['union'])
	l.append(data['disaster'])
	l.append(data['worldstatus'])
	l.append(data['trick'])
	l.append(data['qanda'])		

	return JSONResponse(l)

def get_help(request):
	topic=request.POST.get('topic')
	if topic=='story':
		age_id=int(ServerStatus.objects.get(name='age_id').value)
		response_string=render_to_string('help/story_1.html')
		if age_id>=2:
			response_string+=render_to_string('help/story_2.html',{'middle_age_start':ServerStatus.objects.get(name='middle_age_start').value})
		if age_id>=3:
			response_string+=render_to_string('help/story_3.html',{'industrialism_start':ServerStatus.objects.get(name='industrialism_start').value})
		if age_id>=4:
			response_string+=render_to_string('help/story_4.html')
		
		if request.method=='POST' and request.POST.get('overview')==True:
			response_string+=render_to_string('help/story_overview.html')
		return HttpResponse(response_string)

	elif topic=='research':
		return render_to_response('help/research.html',{'patent_enabled':bool(int(ServerStatus.objects.get(name='patent_enabled').value)) })
	
	elif topic=='yourstatus':
		return render_to_response('help/yourstatus.html',{'money_enabled':bool(int(ServerStatus.objects.get(name='money_enabled').value)) , 'mechanical_energy_enabled':bool(int(ServerStatus.objects.get(name='mechanical_energy_enabled').value))})

	elif topic=='item':
		return render_to_response('help/item.html',{'patent_enabled':bool(int(ServerStatus.objects.get(name='patent_enabled').value)) , 'bank_enabled':bool(int(ServerStatus.objects.get(name='bank_enabled').value)) })

	elif topic=='patent':
		patent_enabled=int(ServerStatus.objects.get(name='patent_enabled').value)
		if patent_enabled==1:
			return render_to_response('help/patent.html')
		else:
			return JSONResponse(u'This feature was locked.')

	elif topic=='mailbox':
		return render_to_response('help/mailbox.html',{'money_enabled':bool(int(ServerStatus.objects.get(name='money_enabled').value)), 'union_enabled':bool(int(ServerStatus.objects.get(name='bank_enabled').value)) })
		
	elif topic=='economy':
		market_enabled=int(ServerStatus.objects.get(name='market_enabled').value)
		bank_enabled=int(ServerStatus.objects.get(name='bank_enabled').value)
		patent_enabled=int(ServerStatus.objects.get(name='patent_enabled').value)
		if market_enabled+bank_enabled+patent_enabled==0:
			return JSONResponse(u'This feature was locked.')

		if market_enabled:
			response_string=render_to_string('help/economy_market.html',{ 'tax_rate':int(float(ServerStatus.objects.get(name='tax_rate').value)*100) })
		if bank_enabled:
			response_string+=render_to_string('help/economy_bank.html')
		if patent_enabled:
			response_string+=render_to_string('help/economy_patent.html',{ 'tax_rate':int(float(ServerStatus.objects.get(name='tax_rate').value)*100) })

		return HttpResponse(response_string)

	elif topic=='union':
		union_enabled=int(ServerStatus.objects.get(name='union_enabled').value)
		if union_enabled==1:
			return render_to_response('help/union.html')
		else:
			return JSONResponse(u'This feature was locked.')

	elif topic=='disaster':
		return render_to_response('help/disaster.html')

	elif topic=='worldstatus':
		return render_to_response('help/worldstatus.html',{ 'much_pollution':int(ServerStatus.objects.get(name='age_id').value)>=4 }) #check from age >= 4

	elif topic=='trick':
		return render_to_response('help/trick.html')		#make it static

	elif topic=='qanda':
		return HttpResponse(render_to_string('help/qanda.html',{'q_and_a_list': QuestionAnswer.objects.all()}).replace('\n','<br/>'))	#system added by admin page
	
	
	else:
		return JSONResponse(u'Does not have this topic.')

def next_item(request):
	ownership_id=request.POST.get('ownership_id')
	try:
		item=Ownership.objects.get(id=ownership_id)
	except ObjectDoesNotExist:
		return JSONResponse({'success':False,'message':u'ขออภัย ไม่พบไอเทมของคุณ'})
	
	result=[]
	this_item=item.item
	for this_formula in Formula.objects.all():
		ok=False
		for an_item in this_formula.components.all():
			if an_item==this_item:
				ok=True
				break
		if not ok:
			for a_type in this_formula.component_types.all():
				if a_type in this_item.item_types.all():
					ok=True
					break
		if ok:
			for a_result in this_formula.results.all():
				result.append(a_result.name)
	if result==[]:
		return JSONResponse({'success':True,'message':u'ขอโทษจริงๆ ข้าจำไม่ได้ว่าไอเทมนี้จะเอาไปทำอะไรได้'})
	else:
		x=randint(0,len(result)-1)
		return JSONResponse({'success':True,'message':u'ข้าจำได้ว่า ไอเทมนี้สามารถนำไปใช้สร้าง <br/>'+result[x]})
		
		

