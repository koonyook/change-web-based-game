# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from newtype.helpers.http import JSONResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.urlresolvers import reverse
from newtype.helpers.decorators import post_or_redirect_to_front
from newtype.helpers.engine import execute_effect
from newtype.helpers.trim_time import trim_time
from django.utils import simplejson
from random import randint
from django.core.exceptions import ObjectDoesNotExist
# Load models
from newtype.core.models import Location, ActiveEffect, ResearchLog, ServerStatus, Weather, Player, Union, Ownership, Formula, Harvesting, Rarity, Formulas_Effects, PollutionState, Result
from newtype.chart.models import State
from newtype.patent.models import Patent
from newtype.helpers.item_dict import item_dict
# Create your views here.

@login_required
def main(request):
    """docstring for main"""
    age_id = int(ServerStatus.objects.get(name='age_id').value)
    age = 'stoneage.css'
    if age_id == 1:
        age = 'stoneage.css'
    elif age_id == 2:
        age = 'woodage.css'
    elif age_id == 3:
        age = 'insdustage.css'
    elif age_id == 4:
        age = 'darkage.css'
    elif age_id == 5:
        age = 'renaissanceage.css'
    return render_to_response('core/main.html', {
            'css_age': '/media/css/'+age,
        });

@post_or_redirect_to_front
def login(request):
    """docstring for login"""
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user != None:
        if user.is_active:
            auth.login(request, user)
            request.session['state'] = 'player'
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('newtype.core.views.main'))
        else:
            # Return a 'disabled account' error message
            return HttpResponseRedirect(reverse('newtype.front.views.front'))
    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect(reverse('newtype.front.views.front'))

def cron(request):
    """cron this view every hour"""
    # Calculate base resources modifier
    natural_resources = float(ServerStatus.objects.get(name='natural_resources').value)
    max_natural_resources = float(ServerStatus.objects.get(name='max_natural_resources').value)
    base_modifier = natural_resources / max_natural_resources

    # Natural resources regeneration   
    natural_resources_regeneration_rate = int(ServerStatus.objects.get(name='natural_resources_regeneration_rate').value)
    ServerStatus.modify_natural_resources( base_modifier*natural_resources_regeneration_rate )
    
    # Pollutions degeneration
    air_pollution_degeneration_rate = int(ServerStatus.objects.get(name='air_pollution_degeneration_rate').value)
    earth_pollution_degeneration_rate = int(ServerStatus.objects.get(name='earth_pollution_degeneration_rate').value)
    water_pollution_degeneration_rate = int(ServerStatus.objects.get(name='water_pollution_degeneration_rate').value)
    air_pollution = ServerStatus.objects.get(name='air_pollution')
    earth_pollution = ServerStatus.objects.get(name='earth_pollution')
    water_pollution = ServerStatus.objects.get(name='water_pollution')
    air_pollution.value = unicode( int(air_pollution.value) - int( base_modifier * air_pollution_degeneration_rate ) )
    earth_pollution.value = unicode( int(earth_pollution.value) - int( base_modifier * earth_pollution_degeneration_rate ) )
    water_pollution.value = unicode( int(water_pollution.value) - int( base_modifier * water_pollution_degeneration_rate ) )
    if int(air_pollution.value) < 0:
        air_pollution.value = unicode(0)
    if int(water_pollution.value) < 0:
        water_pollution.value = unicode(0)
    if int(earth_pollution.value) < 0:
        earth_pollution.value = unicode(0)
    air_pollution.save()
    earth_pollution.save()
    water_pollution.save()
    
    # Player statuses regeneration
    for player in Player.objects.all():
        player.energy += player.get_regeneration_rate()
        max_energy = player.get_max_energy()
        if player.energy > max_energy:
            player.energy = max_energy
        player.save()
        
    # Union statuses regeneration
    for union in Union.objects.all():
        union.energy += union.get_regeneration_rate()
        max_energy = union.get_max_energy()
        if union.energy > max_energy:
            union.energy = max_energy
        union.save()
        
    # Effects
    from newtype.helpers.feeds import feed_weather, earthquake, fill_clean_energy, random_disease
    feed_weather()
    earthquake()
    fill_clean_energy()
    random_disease()
    
    # PollutionState Effects
    PollutionState.cron_effects()
    
    # Update chart
    State.update()    
    
    # Update cron time
    from datetime import datetime
    last_cron = ServerStatus.objects.get(name="last_cron")
    last_cron.value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_cron.save()
        
    return HttpResponse('Cron tasks finished')
    
def server_status(request):
    """docstring for server_status"""
    statuses = dict()
    for status in ServerStatus.objects.all():
        statuses[status.name] = status.value
    statuses['weather']=Weather.objects.get(id=ServerStatus.objects.get(name='weather_id').value).name
    return JSONResponse( statuses )
    
def weather(request):
    """docstring for weather"""
    weather_id = int(ServerStatus.objects.get(name='weather_id').value)
    return JSONResponse( Weather.objects.get(id=weather_id).name )
    
#
# User related view (/user/*)
#
@login_required
def harvest(request):
    """docstring for harvest"""
    from newtype.helpers.item_dict import item_dict
    
    response = request.user.player.harvest()        
    if response['item']:
        response['item'] = item_dict(response['item'])
        response['item']['level'] = response['level']
    
    return JSONResponse(response)
    
    # if item is not None:
    #     return JSONResponse({'success':True, 'item':item_dict(item)})
    # else:
    #     return JSONResponse({'success':False,'item':'','message':u'คุณมีพลังงานไม่เพียงพอในการหาทรัพยากร'})

@login_required
def menu(request):
    """docstring for menu"""
    max_energy = request.user.player.get_max_energy()
    if request.user.player.energy > max_energy:
        request.user.player.energy = max_energy
        request.user.player.save()
    
    from datetime import datetime
    request.user.player.last_active = datetime.now()
    request.user.player.save()
    hud = {
        'name': request.user.username,
        'union': request.user.player.union,
        'money': request.user.player.money,
        'energy': request.user.player.energy,
        'max_energy': max_energy,
        'mechanical_energy': request.user.player.mechanical_energy,
        'max_mechanical_energy': request.user.player.get_max_mechanical_energy(),
        'used_storage':request.user.player.get_used_space(),
        'storage':request.user.player.get_total_space(),
    }
    
    # If there's union, convert it to dict to make it serializable
    union = request.user.player.union
    if union != None:
        hud['union'] = union.__dict__
        hud['union']['_state'] = None # Unserializable workaround
        hud['union']['used_storage'] = request.user.player.union.get_used_space()
    return JSONResponse(hud)
    
@login_required
def location(request):
    """docstring for location"""
    player = request.user.player
    if request.method == 'POST':
        if request.POST.has_key('location'):
            try:
                player.travel_to( Location.objects.get(name=request.POST['location']) )
            except Exception:
                return HttpResponse('') # Blank response mean traveling failed
    
    if player.location.name.lower() != 'union':
        request.session['state'] = 'player'
                
    return render_to_response('location/' + player.location.name.lower() + '.html')

@login_required
def items(request):
    """docstring for items"""
    Ownership.clear_expired_items()
    
    if request.session['state'] == 'player':
        ownerships = Ownership.objects.filter(player=request.user.player)
        # items = request.user.player.items
    else:
        ownerships = Ownership.objects.filter(union=request.user.player.union)
        # items = request.user.player.union.items
        
    if (request.method == 'POST') and (request.POST['search'] is not None):
        ownerships = ownerships.filter(item__name__icontains=request.POST['search']) | ownerships.filter(item__description__icontains=request.POST['search'])
        
    items = list()
    for ownership in ownerships:
        item = item_dict(ownership)
        # item['ownership_id'] = ownership.id
        # item['max_durability'] = item['durability']
        # item['durability'] = ownership.durability       #koon debug here
        # item['level'] = ownership.level
        # item['is_avalible'] = bool(ownership.is_available)
        # item['expire_at'] = str(ownership.expire_at)
        item['type'] = [item_type.name for item_type in ownership.item.item_types.all()]
        if ownership.item.use_effects.all().count()>0:
            item['usable'] = True
        else:
            item['usable'] = False
        if u'เทคโนโลยี' in item['type']:
            item['is_technology'] = True
        else:
            item['is_technology'] = False
        item['icon_url']=ownership.item.get_full_icon_url()
        '''
        if item['icon_url']=='':
            item['icon_url']=ServerStatus.objects.get(name='images_path').value+'items/icons/'+'icon_box'+'.png'
        else:
            item['icon_url']=ServerStatus.objects.get(name='images_path').value+'items/icons/'+item['icon_url']+'.png'
        '''
        items.append( item )
        
    return JSONResponse( items )
    
@login_required
def state(request):
    """docstring for state"""
    if (request.method == 'POST') and (request.POST.get('state', False)):
        if request.POST['state'] == 'union' and request.user.player.union != None:
            request.session['state'] = 'union'
        else:
            request.session['state'] = request.POST['state']
    return HttpResponse(request.session['state'])
    
def decode(value):
    value=eval(value)
    print value
    data=u''
    for k in value.keys():
        if k=='max_energy':
            data=data+u'พลังงานสูงสุด'
        elif k=='regeneration_rate':
            data=data+u'อัตราการฟื้นฟู'
        elif k=='research_cost':
            data=data+u'ค่าวิจัย'
        elif k=='travel_cost':
            data=data+u'ค่าเดินทาง'
        elif k=='chance':
            data=data+u'โอกาสติดโรคลดลงเหลือ'
        elif k=='step':
            data=data+u'ระดับ'
        elif k=='storage':
            data=data+u'พื้นที่'
        elif k=='name':
            data=data+u'สถานะ'
        elif k=='vehicle':
            data=data+u'พาหนะ'
        else:
            data=data+k
        
        if k=='chance':
            data=data+' : '+str(value[k])+'% <br/>'        
        elif type(value[k])==type(1) and value[k]>0 and k!='step':
            data=data+' : +'+str(value[k])+' <br/>'
        else:
            data=data+' : '+unicode(value[k])+' <br/>'
    return data

@login_required
def status(request):
    """docstring for status"""
    effects = list()
    for effect in [active_effect for active_effect in ActiveEffect.objects.filter(player=request.user.player)]:
        tmp=effect.effect
        effect=effect.__dict__
        effect['description']=tmp.description
        effect['name']=tmp.name
        effect['expire_at']=trim_time(effect['expire_at'])
        effect['_state'] = None
        effect['_effect_cache'] = None
        effect['value']=decode(effect['value'])
        if effect['expire_at']!=u'None':
            effect['value']=effect['value']+u'หมดเวลา : '+effect['expire_at']+'<br/>'
        if effect['times_left']!=None:
            effect['value']=effect['value']+u'ใช้ได้อีก : '+unicode(effect['times_left'])+u' ครั้ง<br/>'
        effects.append( effect )
    status = {
        'regeneration_rate': request.user.player.get_regeneration_rate(),
        'research_cost': request.user.player.get_research_cost(),
        'travel_cost': request.user.player.get_travel_cost(),
        # effect value returned is still wrong, but don't care since we don't use it anyway.
        'effects': effects,
        'harvest_cost': request.user.player.get_harvest_cost(),
    }
    if request.user.player.union != None:
        status['union'] = request.user.player.union.__dict__
        status['union']['_state'] = None
    else:
        status['union'] = None
    return JSONResponse(status)
    
@login_required
def research_log(request):
    """docstring for research_log"""
    if request.session['state'] == 'player':
        research_logs = ResearchLog.objects.filter(player=request.user.player)
    else:
        research_logs = ResearchLog.objects.filter(player=request.user.player.union)
    response = list()
    for research_log in research_logs:
        log = dict()
        # if research_log.union != None:
        #     log['union'] = research_log.union.__dict__
        # else:
        #     log['union'] = None
        # if research_log.player != None:
        #     log['player'] = research_log.player.__dict__
        # else:
        #     log['player'] = None
        log['items'] = list()
        for item in research_log.items.all():
            each_item = {
                'name': item.name,
                'icon_url': item.get_full_icon_url(),
            }
            log['items'].append( each_item )
        log['weather'] = research_log.weather.name
        if research_log.formula != None:
            log['formula'] = research_log.formula.name
            # patent = Patent.objects.get(formula=research_log.formula)
            patent = research_log.formula.patent
            log['patent_id'] = patent.id
            log['registrable'] = (patent.status==0) and (patent.regis_cost!=None)
        else:
            log['formula'] = None
            log['patent_id'] = None
            log['registrable'] = False
        log['time'] = trim_time( research_log.time )
        log['is_success'] = bool(research_log.is_success)
        response.append( log )
    return JSONResponse(response)
        
@login_required
@post_or_redirect_to_front
def use_item(request):
    """docstring for use_item"""    
    try:
        ownership = Ownership.objects.get(id=request.POST['ownership_id'])
    except ObjectDoesNotExist:
        return HttpResponse(u'invalid ownership_id')
    # Validation
    if request.session['state'] == 'player':
        # Player mode
        if ownership.player != request.user.player:
            return HttpResponse(u'invalid player') # Validation failed
    else:
        # Union mode
        if ownership.union != request.user.player.union:
            return HttpResponse(u'invalid union') # Validation failed

    item = ownership.item
    item.create_pollutions()
    output = []
    using_success = True
    for use_effect in item.items_useeffects_set.all():
        # message, none
        result = execute_effect(use_effect.effect, request=request, value=use_effect.value)
        output.append( result )
        if result['error'] is True:
            using_success = False
    
    if using_success:
        ownership.durability -= 1
        if ownership.durability <= 0:
            ownership.delete()            
        else:
            ownership.save()
        
    return JSONResponse( output )
    
@login_required
@post_or_redirect_to_front
def remove_item(request):
    """docstring for remove_item"""
    try:
        ownership = Ownership.objects.get(id=request.POST['ownership_id'])
    except ObjectDoesNotExist:
        return JSONResponse({'success':False,'message': u'invalid ownership_id'})    
    # Validation
    if request.session['state'] == 'player':
        # Player mode
        if ownership.player != request.user.player:
            return JSONResponse({'success':False,'message':u'invalid player'}) # Validation failed
    else:
        # Union mode
        if ownership.union != request.user.player.union:
            return JSONResponse({'success':False,'message':u'invalid union'}) # Validation failed
            
    ownership.item.create_pollutions()
    ownership.delete()
        
    return JSONResponse({'success':True,'message':u'ไอเทมถูกทิ้งสู่สิ่งแวดล้อม'})

@login_required
@post_or_redirect_to_front
def research(request):
    """docstring for research"""
    research_log = ResearchLog(
        weather = Weather.objects.get(id=ServerStatus.objects.get(name='weather_id').value)
    )
    research_log.save()
    
    #ownership_ids = simplejson.loads( request.POST['items'] )
    ownership_ids = request.POST.getlist('items')
    if request.POST.get('catalyst_id') != None:
        catalyst = Ownership.objects.get(id=request.POST['catalyst_id']).item
    else:
        catalyst = None
    
    if request.session['state'] == 'player':
        entity = request.user.player
        research_log.player = entity
    else:
        entity = request.user.player.union
        research_log.union = entity
        
    count_blank=ownership_ids.count(u'')    
    for i in range(count_blank):
        ownership_ids.remove(u'')
    # print ownership_ids
    
    try:
        ownerships = [ Ownership.objects.get(id=ownership_id) for ownership_id in ownership_ids ]
    except ObjectDoesNotExist:
        return JSONResponse({'is_success': False, 'message': u'ไอเทมไม่ถูกต้อง'}) # invalid ownership_id
        
    if ownerships is None:
        return JSONResponse({'is_success': False, 'message': u'ต้องป้อนไอเทมอย่างน้อย 1 ชิ้น'}) # Need to specify at least 1 ownership
        
    for ownership in ownerships:
        if not ownership.is_available:
            return JSONResponse({'is_success': False, 'message': u'ไอเทมไม่ถูกต้อง'}) # Items not available
            
    if not entity.replenish_energy(-entity.get_research_cost()): # Not enough energy
        return JSONResponse({'is_success': False, 'message': u'คุณมีพลังงานไม่พอที่จะทำการวิจัย'})
            
    total_air_pollution = 0
    total_earth_pollution = 0
    total_water_pollution = 0
    for ownership in ownerships:
        item = ownership.item
        research_log.items.add(item)
        total_air_pollution += item.air_pollution
        total_water_pollution += item.water_pollution
        total_earth_pollution += item.earth_pollution

    research_result = entity.research(ownerships=ownerships, catalyst=catalyst, request=request)
    research_log.is_success = research_result['is_success']
    
    response = {
        'is_success': research_result['is_success'],
        'message': research_result['message'],
        'level': research_result['level'],
        'air_pollution': total_air_pollution,
        'water_pollution': total_water_pollution,
        'earth_pollution': total_earth_pollution,
    }
    '''
    if research_log.is_success:
        is_founder = research_result['formula'].patent.set_founder( request.user.player )
        response['is_founder'] = is_founder
    '''
    response['is_founder'] = False
    if research_result['formula'] != None:
        for formula_effect in Formulas_Effects.objects.filter(formula=research_result['formula']):
            execute_effect(effect=formula_effect.effect, request=request, value=formula_effect.value)
        
        response['is_founder'] = research_result['formula'].patent.set_founder( request.user.player )
        from newtype.helpers.item_dict import item_dict
        formula = research_result['formula']
        response['formula'] = {
            'name': formula.name,
            'description': formula.description,
            'items': list(),
        }
        for item in formula.results.all():
            this_item = item_dict(item)
            this_item['quantity'] = Result.objects.get(formula=formula, item=item).quantity
            this_item['level'] = research_result['level']
            if catalyst != None:
                this_item['quantity'] *= int(float(catalyst.research_modifier)/100.0)
            response['formula']['items'].append( this_item )
                    
        response['space_needed'] = formula.get_results_storage_cost()
        
        research_log.formula = formula
    
    research_log.save()
        
    return JSONResponse(response)
         
