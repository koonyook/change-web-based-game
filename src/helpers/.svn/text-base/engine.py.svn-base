# -*- coding: UTF-8 -*-
from newtype.core.models import ServerStatus, ActiveEffect, Ownership, Formula, Effect, Player
from newtype.helpers.item_dict import item_dict
from newtype.helpers.trim_time import trim_time
from newtype.mail.views import send_alert
from django.core.exceptions import ObjectDoesNotExist
from random import random
import datetime

def get_online_players():
    mylist = list()
    players = Player.objects.all()
    from datetime import datetime, timedelta
    for player in players:
        if (datetime.now() - player.last_active) <= timedelta(minutes=5):
            mylist.append(player.user.username)
    return unicode(",".join(mylist).lower())

def give_old_patent():						#give patent to the founder free
    for this_formula in Formula.objects.all():
        this_patent=this_formula.patent
        if this_patent.founder!=None and this_patent.regis_cost!=None:
            this_patent.status=1
            this_patent.regis_at=datetime.datetime.now()
            this_patent.set_owner(this_patent.founder)
            this_patent.save()
            send_alert(this_patent.founder,u'สิทธิบัตรฟรี',u'คุณได้รับสิทธิบัตร '+this_patent.formula.name+u' โดยไม่ต้องเสียค่าธรรมเนียม เพราะว่าคุณเป็นผู้ค้นพบคนแรก')

def execute_effect(effect, request=None, value=None, player=None):
    """docstring for execute"""
    if value is None:
        value = effect.value
    
    if request!=None:
        player=request.user.player

    # Executing rules
    if effect.effect_type.name == 'normal':
        if effect.name == 'change_ServerStatus':
            data=eval(value)
            this_status=ServerStatus.objects.get(name=data['name'])
            
            if data['name']=='patent_enabled' and this_status.value=='0':
                give_old_patent()
            
            if data['name']=='age_id' and int(this_status.value)>=int(data['data']):
                return {'error':False,'type':'null','message':''}

            this_status.value=unicode(data['data'])
            this_status.save()
            
            if data['name']== 'age_id' and data['data']=='2' and ServerStatus.objects.get(name='middle_age_start').value=='0':
                this_status2=ServerStatus.objects.get(name='middle_age_start')
                this_status2.value=trim_time(datetime.datetime.now())          #I will change it later
                this_status2.save()
            elif data['name']== 'age_id' and data['data']=='3' and ServerStatus.objects.get(name='industrialism_start').value=='0':
                this_status2=ServerStatus.objects.get(name='industrialism_start')
                this_status2.value=trim_time(datetime.datetime.now())          #I will change it later
                this_status2.save()  
            return {'error':False,'type':'null','message':''}
        elif effect.name == 'modify_natural_resource':
            data=eval(value)
            natural_resource=int(data['natural_resource'])
            ServerStatus.modify_natural_resource(natural_resource)
            return {'error':False,'type':'message','message':u'คุณได้คืนทรัพยากรธรรมชาติกลับคืนสู่โลกแล้ว'}
        elif effect.name == 'modify_energy':
            data=eval(value)
            energy=data.get('energy')
            mechanical_energy=data.get('mechanical_energy')
            if energy!=None:
                player.replenish_energy(int(energy))             #positive & negative
                if int(energy)>0:
                    return {'error':False,'type':'message','message':u'พลังงานของคุณเพิ่มขึ้นแล้ว'}
                else:
                    return {'error':False,'type':'message','message':u'พลังงานของคุณลดลง'}
            if mechanical_energy!=None:
                player.replenish_mechanical_energy(int(mechanical_energy))   #positive & negative
                if int(mechanical_energy)>0:
                    return {'error':False,'type':'message','message':u'พลังงานขกรกลของคุณเพิ่มขึ้นแล้ว'}
                else:
                    return {'error':False,'type':'message','message':u'พลังงานจักรกลของคุณลดลง'}

        elif effect.name == 'cure':
            data=eval(value)
            time_rate=int(data.get('time_rate'))
            
            queryset=player.activeeffect_set.filter(effect__name='disease')
            for e in queryset:
                e.expire_at=datetime.datetime.now()+(e.expire_at-datetime.datetime.now())*(time_rate/100)
                e.save()
            
            return {'error':False,'type':'null','message':''}
            
    elif effect.effect_type.name == 'register':
        data=eval(value)
        if request==None:
            this_active=ActiveEffect(effect=Effect.objects.get(name=data['regis_effect']),player=player)
        else:
            this_active=ActiveEffect(effect=Effect.objects.get(name=data['regis_effect']),player=player)
        expiration=data.get('expiration')
        if expiration!=None:
            this_active.expire_at=datetime.datetime.now()+expiration
        times_left=data.get('times_left')
        if times_left!=None:
            this_active.times_left=int(times_left)
            
        this_active.value=unicode(data['data'])

        chance=data.get('chance')
        if chance!=None:
            if effect.name == 'regis_disease':
                try:
                    immunity=player.activeeffect_set.get(effect__name='immunity').__dict__
                    immunity=eval(immunity['value'])['chance']
                except ObjectDoesNotExist:
                    immunity=0
                chance=chance*(100-immunity)/100
            
            if random()*100 > int(chance):
                return {'error':False,'type':'message','message':u'ไม่เกิดอะไรขึ้นกับตัวคุณ'}    
        
        mechanical_energy=data.get('mechanical_energy')
        if mechanical_energy!=None:
            mechanical_energy=int(mechanical_energy)
            success=player.replenish_mechanical_energy(mechanical_energy)
            if not success:
                return {'error':True,'type':'message','message':u'คุณมีพลังงานจักรกลไม่เพียงพอ'}                  
        
        if effect.name == 'regis_immunity':
            try:
                immunity=player.activeeffect_set.get(effect__name='immunity')
                immunity.delete()
            except ObjectDoesNotExist:
                pass
        
        if effect.name == 'regis_modify_storage':
            queryset=player.activeeffect_set.filter(effect__name='modify_storage')
            for e in queryset:
                if eval(e.value)['step'] == (this_active.value)['step'] :
                    return {'error':True,'type':'message','message':u'ไอเทมนี้ไม่สามารถใช้ซ้ำได้'}
        
        if effect.name == 'regis_vehicle':
            try:
                vehicle=player.activeeffect_set.get(effect__name='vehicle')
                vehicle.delete()
            except ObjectDoesNotExist:
                pass

        this_active.save()
        if effect.name == 'regis_disease':
            return {'error':False,'type':'message','message':u'คุณได้รับเชื้อ และติดโรค'}
        elif effect.name == 'regis_immunity':
            return {'error':False,'type':'message','message':u'คุณมีภูมิคุ้มกันแล้ว'}
        elif effect.name == 'regis_modify_storage':
            return {'error':False,'type':'message','message':u'พื้นที่เก็บของของคุณได้เพิ่มขึ้นแล้ว'}
        elif effect.name == 'regis_vehicle':
            return {'error':False,'type':'message','message':u'คุณได้ใช้พาหนะแล้ว'}
        elif effect.name == 'regis_general':
            return {'error':False,'type':'message','message':u'คุณได้รับสถานะ '+data['data'].get('name')}

    elif effect.effect_type.name == 'active':
        return {'error':True,'type':'message','message':'Please contact staff for this error'}

    elif effect.effect_type.name == 'special':
        if effect.name == 'mini_research_kit':
            return {'error':False,'type':'null','message':''}
        elif effect.name == 'harvest':
            ownership_id=request.POST['ownership_id']
            try:
                this_ownership=Ownership.objects.get(id=ownership_id)
            except ObjectDoesNotExist:
                return {'error':True,'type':'message','message':'ownership_id invalid'}
            unlocker=this_ownership.item
            response=player.harvest(unlocker)
            if response['item']!=None:
                response['item'] = item_dict(response['item'])
                return {'error':False,'type':'harvest_response','message':response}
            else:
                return {'error':True,'type':'message','message':response['message']}
            '''
            if item==None:
                return {'error':True,'type':'message','message':'You cannot use this item for harvesting here.'}
            else:
                return {'error':False,'type':'show_item','message':item_dict(item)}
            '''
    elif effect.effect_type.name == 'hold':
        if effect.name == 'generate_clean_energy':
            pass                        # wait for cron (execute path may be in cron)
        elif effect.name == 'disaster_modifier':
            pass                        # do not have execute path
    elif effect.effect_type.name == 'eval' :      #do not have this effect_type now
        try:
            eval(value)
        except Exception:
            raise
            
    return dict()