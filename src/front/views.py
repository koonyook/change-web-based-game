# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from newtype.helpers.decorators import post_or_redirect_to_front
from newtype.helpers.http import JSONResponse
from newtype.helpers.engine import get_online_players
from newtype.core_union.models import SettingUnion
from newtype.core.models import Item
from logging import debug
from newtype.mail.views import send_alert
from newtype.core.models import Player, ServerStatus
@post_or_redirect_to_front
def register(request):
    """Registration handler"""
    from newtype.front.forms import RegisterForm
    from newtype.core.models import Player
    
    form = RegisterForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
        # Process the data in form.cleaned_data
        try:
            player=Player.register(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email'],
                geo_location = (form.cleaned_data['latitude'], form.cleaned_data['longitude'])
            )
            SettingUnion.objects.create(player=player)
            send_alert(player,u'ยินดีต้อนรับเข้าสู่เกม Change เปลี่ยนคุณ เปลี่ยนโลก',u'ส่วนที่คุณอยู่ในขณะนี้คือส่วนของกล่องรับข้อความ ที่จะคอยรับข่าวสารจากผู้ดูแลระบบ และ จากเพื่อนร่วมโลกของคุณ\n**เพื่อการแสดงผลที่ถูกต้อง เราแนะนำให้ใช้ Firefox3.5 ขึ้นไปในการเล่นเกม<a href="http://www.firefox.com/">[Download]<a/>\n**และคุณควรเข้า fullscreen mode โดยการกด F11\nขั้นแรก คุณต้องรู้จักวิธีเล่นก่อน โดยการ คลิกที่เมนูไอเทมด้านล่างซ้าย แล้ว "คลิกขวา" ที่ไอเทม หนังสือตัวช่วย แล้วคลิกที่ "อ่าน" เพื่อศึกษาวิธีการเล่นเกม\n\nขอให้สนุกกับเกมนะครับ')
            own=player.add_item(Item.objects.get(name=u'หนังสือผู้ช่วย'))
            own.is_available=False
            own.save()
        # except Exception as e:
        except Exception:
            # debug(e)
            #print e
            # raise
            return JSONResponse({
                'username': 'Duplicated username',
                # 'password': 'Unknow Error',
                # 'email': 'Unknow Error',
                # 'latitude': 'Unknow Error',
                # 'longitude': 'Unknow Error',
            })
            
        return JSONResponse({})
    else:
        errors = {}        
        for field in form.errors.keys():
            if form.errors[field] is not None:
                errors[field] = ''
                for error in form.errors[field]:
                    errors[field] += unicode(error) # + '\n'
            
        return JSONResponse(errors)
    
def front(request):
    """Front page"""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('newtype.core.views.main'))
    else:
        register_url = reverse(register)
        age_id = int(ServerStatus.objects.get(name='age_id').value)
        age = 'stoneage.css'
        if age_id == 1:
            age = 'stoneage'
        elif age_id == 2:
            age = 'woodage'
        elif age_id == 3:
            age = 'insdustage'
        elif age_id == 4:
            age = 'darkage'
        elif age_id == 5:
            age = 'renaissanceage'
        return render_to_response('front/front.html', {
            'register_url': register_url,
            'online_players': get_online_players(),
			'logo_img_url': '/media/images/'+age+'/logo.png',
        });

def overview(request):
    """Overview page"""
    
    return render_to_response('front/overview.html');
