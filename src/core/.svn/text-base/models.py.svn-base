# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.html import escape
from datetime import datetime, timedelta
from random import random, randint
from django.core.exceptions import ObjectDoesNotExist

#
# Server status models
#
class PollutionState(models.Model):
    """(PollutionState description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    next_at = models.IntegerField()
    previous_at = models.IntegerField()
    
    @staticmethod
    def shift(percentage):
        """docstring for shift_state"""
        percentage = int(percentage)
        state_id = ServerStatus.objects.get(name='pollution_state_id')
        state = PollutionState.objects.get(id=int(state_id.value))
        
        if state.name == "Critical":
            if (percentage <= state.prevous_at) and ( ServerStatus.objects.get(name='environvent_found').value != '0' ):
                state_id.value = int(state_id.value) - 1
                state.disable()
                PollutionState.objects.get(id=int(state_id.value)).enable()
                state_id.save()
        elif state.name == "Normal":
            if percentage >= state.next_at:
                state_id.value = int(state_id.value) + 1
                state.disable()
                PollutionState.objects.get(id=int(state_id.value)).enable()
                state_id.save()
        else:
            if percentage >= state.next_at:
                state_id.value = int(state_id.value) + 1
                state.disable()
                PollutionState.objects.get(id=int(state_id.value)).enable()
                state_id.save()
            elif percentage <= state.prevous_at:
                state_id.value = int(state_id.value) - 1
                state.disable()
                PollutionState.objects.get(id=int(state_id.value)).enable()
                state_id.save()
                
    def enable(self):
        """docstring for enable"""
        if self.name == 'Warning':
            # Shift to Dark age
            age_id = ServerStatus.objects.get(name='age_id')
            if int(age_id.value) in [1, 2, 3]:
                age_id.value = 4
                age_id.save()
            
            from newtype.helpers.engine import execute_effect
            disease = Effect.objects.get(name='regis_disease')
            value = '''{
                'regis_effect': 'disease',
                'chance': 100,
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
            
            disease_chance = ServerStatus.objects.get(name='disease_chance')
            disease_chance.value = int(disease_chance.value) + 30
            disease_chance.save()
        elif self.name == 'Dangerous':
            for player in Player.objects.all():
                money = float(player.money)
                player.money = int( money/2 )
                player.save()
            
            tax_rate = ServerStatus.objects.get(name='tax_rate')
            tax_rate.value = float(tax_rate.value) + 0.04
            tax_rate.save()
        elif self.name == 'Emergency':
            disaster_modifier = ServerStatus.objects.get(name='disaster_modifier')
            disaster_modifier.value = float(disaster_modifier.value) + 0.5
            disaster_modifier.save()
            from newtype.helpers.feed import big_disaster
            big_disaster()
        elif self.name == 'Critical':
            pass
        
    def disable(self):
        """docstring for disable"""
        if self.name == 'Warning':
            # Shift to Renaissance age
            age_id = ServerStatus.objects.get(name='age_id')
            if int(age_id.value) == 4:
                age_id.value = 5
                age_id.save()
            
            disease_chance = ServerStatus.objects.get(name='disease_chance')
            disease_chance.value = int(disease_chance.value) - 30
            disease_chance.save()
        elif self.name == 'Dangerous':
            tax_rate = ServerStatus.objects.get(name='tax_rate')
            tax_rate.value = float(tax_rate.value) - 0.04
            tax_rate.save()
        elif self.name == 'Emergency':
            disaster_modifier = ServerStatus.objects.get(name='disaster_modifier')
            disaster_modifier.value = float(disaster_modifier.value) - 0.5
            disaster_modifier.save()
        elif self.name == 'Critical':
            game_over_date = ServerStatus.objects.get(name="game_over_date")
            game_over_date.value = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
            game_over_date.save()
            pass
            
    @staticmethod
    def cron_effects():
        """docstring for cron_effects"""
        state_id = int(ServerStatus.objects.get(name='pollution_state_id').value)
        state = PollutionState.objects.get(id=state_id)
        
        if state.name == "Dangerous":
            last_cron = ServerStatus.objects.get(name='last_cron').value
            last_cron = datetime.strptime(last_cron, "%Y-%m-%d %H:%M:%S")
            
            if datetime.now() - last_cron < timedelta(days=1):
                for player in Player.objects.all():
                    money = float(player.money)
                    player.money = int( money * 0.95 )
                    player.save()
        elif state.name == "Critical":
            game_over_date = ServerStatus.objects.get(name='game_over_date').value
            game_over_date = datetime.strptime(game_over_date, "%Y-%m-%d %H:%M:%S")
            if datetime.now() > game_over_date:
                game_over = ServerStatus.objects.get(name='game_over')
                game_over.value = 1
                game_over.save()

    def __unicode__(self):
        return unicode(self.name)

class Weather(models.Model):
    """(Weather description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name)

class Age(models.Model):
    """(Age description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name)
        
class ServerEvent(models.Model):
    """(ServerEvent description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name)

class ServerStatus(models.Model):
    """
    Server statues
    Define in initial_data.yaml fixture
    """
    name = models.CharField(max_length=255, db_index=True)
    value = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name_plural = "Server Statuses"
        
    @staticmethod
    def get_value(self, name):
        """docstring for get_value"""
        return ServerStatus.objects.get(name=name).value
    
    @staticmethod
    def check_pollutions_level():
        """docstring for fname"""
        air_pollution = float(ServerStatus.objects.get(name='air_pollution').value)
        water_pollution = float(ServerStatus.objects.get(name='water_pollution').value)
        earth_pollution = float(ServerStatus.objects.get(name='earth_pollution').value)
        max_air_pollution = float(ServerStatus.objects.get(name='max_air_pollution').value)
        max_water_pollution = float(ServerStatus.objects.get(name='max_water_pollution').value)
        max_earth_pollution = float(ServerStatus.objects.get(name='max_earth_pollution').value)
        percentage = (( air_pollution/max_air_pollution ) + ( water_pollution/max_water_pollution ) + ( earth_pollution/max_earth_pollution )) * 100
        PollutionState.shift( percentage )
        
    @staticmethod
    def modify_natural_resources(increment):
        """docstring for modify_resources"""
        natural_resources = ServerStatus.objects.get(name='natural_resources')
        natural_resources_value = int(natural_resources.value) + int(increment)
        max_natural_resources_value = int(ServerStatus.objects.get(name='max_natural_resources').value)
        
        if natural_resources_value < 0:
            natural_resources.value = 0
        elif natural_resources_value > max_natural_resources_value:
            natural_resources.value = max_natural_resources_value
        else:
            natural_resources.value = natural_resources_value
            
        natural_resources.save()
        return natural_resources.value

    def __unicode__(self):
        return unicode(self.name)
        
#
# Items, Effects related models
#
        
class ItemType(models.Model):
    """Item's type"""
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    
    def get_all_item(self):
        s=''
        for item in self.item_set.all():
            s=s+item.name+', '
        return s

    def __unicode__(self):
        return unicode(self.name)

class EffectType(models.Model):
    """(EffectType description)"""
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name)
        
class Effect(models.Model):
    """(Effect description)"""
    name = models.CharField(max_length=255)
    effect_type = models.ForeignKey(EffectType)
    description = models.TextField(blank=True)
    value = models.TextField()

    def __unicode__(self):
        return unicode(str(self.effect_type)+':'+self.name)
        
class StatusModifier(models.Model):
    """(StatusModifier description)"""
    storage_modifier = models.IntegerField(default=0)
    max_energy_modifier = models.IntegerField(default=0)
    max_mechanical_energy_modifier = models.IntegerField(default=0)
    travel_cost_modifier = models.IntegerField(default=0)
    research_cost_modifier = models.IntegerField(default=0)
    regeneration_rate_modifier = models.IntegerField(default=0)
    harvest_cost_modifier = models.IntegerField(default=0)

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u"StatusModifier"

class Item(StatusModifier):
    """(Item description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    item_types = models.ManyToManyField(ItemType, blank=True, null=True)
    # icon_url = models.URLField(verify_exists=True, blank=True, null=True)
    # image_url = models.URLField(verify_exists=True, blank=True, null=True)
    icon_url = models.CharField(blank=True, max_length=255)
    image_url = models.CharField(blank=True, max_length=255)
    research_modifier = models.IntegerField(default=0)
    durability = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    expiration = models.IntegerField(blank=True, null=True, help_text="Avalibility duration in seconds") # In seconds 
    storage_cost = models.IntegerField(default=1)
    air_pollution = models.IntegerField(default=0)
    water_pollution = models.IntegerField(default=0)
    earth_pollution = models.IntegerField(default=0)
    hold_effects = models.ManyToManyField(Effect, through='Items_HoldEffects', related_name='by_holding', blank=True, null=True)
    use_effects = models.ManyToManyField(Effect, through='Items_UseEffects', related_name='by_using', blank=True, null=True)

    def get_item_types_list(self):
        tmp=self.item_types.all().values_list('name')
        ans=[]
        for i in range(len(tmp)):
            ans.append(tmp[i][0])
        return ans
    
    def get_image_tag(self):
        return '<img src="%s" />' % self.get_full_icon_url()
    get_image_tag.allow_tags = True

    def get_full_icon_url(self):
        """docstring for get_full_icon_url"""
        if self.icon_url=='':
            return ServerStatus.objects.get(name='images_path').value+'items/icons/'+'icon_box'+'.png'
        else:
            return ServerStatus.objects.get(name='images_path').value+'items/icons/'+self.icon_url+'.png'
        #return ServerStatus.objects.get(name='images_path').value + self.icon_url
    
    def get_full_image_url(self):
        """docstring for get_full_image_url"""
        return ServerStatus.objects.get(name='images_path').value + self.image_url
        
    def create_pollutions(self, pollution_modifier=1):
        """docstring for create_pollutions"""
        server_status = ServerStatus.objects.get(name='air_pollution')
        server_status.value = int((int(server_status.value) + self.air_pollution) * pollution_modifier)
        server_status.save()
        server_status = ServerStatus.objects.get(name='water_pollution')
        server_status.value = int((int(server_status.value) + self.water_pollution) * pollution_modifier)
        server_status.save()
        server_status = ServerStatus.objects.get(name='earth_pollution')
        server_status.value = int((int(server_status.value) + self.earth_pollution) * pollution_modifier)
        server_status.save()
        ServerStatus.check_pollutions_level()

    def __unicode__(self):
        return unicode(self.name)          #unicode(self.id)+
        
class Items_Effects(models.Model):
    """(Items_Effects description)"""
    item = models.ForeignKey(Item)
    effect = models.ForeignKey(Effect)
    value = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"Items_Effects"

class Items_HoldEffects(Items_Effects):
    """(Item_HoldEffects description)"""
    
    class Meta:
        verbose_name = "Holding Effect"

    def __unicode__(self):
        return u"Item_HoldEffects"

class Items_UseEffects(Items_Effects):
    """(Items_UseEffects description)"""
    
    class Meta:
        verbose_name = "Using Effect"

    def __unicode__(self):
        return u"Items_UseEffects"

#
# Players, Unions related models
#

class Entity(models.Model):
    """Abstract models for Player, Union"""
    storage = models.IntegerField()
    reserve_space = models.IntegerField(default=0)
    energy = models.IntegerField()
    max_energy = models.IntegerField()
    mechanical_energy = models.IntegerField()
    max_mechanical_energy = models.IntegerField()
    research_cost = models.IntegerField()
    regeneration_rate = models.IntegerField()
    money = models.IntegerField(default=0)
    items = models.ManyToManyField(Item, through='Ownership', blank=True, null=True)
    
    def get_used_space(self):
        """docstring for get_used_space"""
        used_space = self.reserve_space
        if self.__class__ == Player:
            ownerships = Ownership.objects.filter(player=self)
        else:
            ownerships = Ownership.objects.filter(union=self)
        for ownership in ownerships:
        # for ownership in self.ownership_set.all():
            used_space += ownership.item.storage_cost
        return used_space
        
    def get_total_space(self):
        """docstring for get_total_space"""
        space = self.storage
        
        for value in [ eval(activeeffect.value) for activeeffect in self.activeeffect_set.all()]:
            if value.has_key('storage'):
                space += value['storage']
                
        return space
        
    def get_free_space(self):
        """docstring for get_free_space"""        
        return self.get_total_space() - self.get_used_space()
        
    def research(self, ownerships, catalyst=None, request=None):
        """docstring for research"""
        have_enough_energy=self.replenish_energy(-self.get_research_cost())  #Koon debug here sef -> self  & replenished -> replenish
        
        if not have_enough_energy:
            return {'is_success': False, 'formula': None, 'message': 'คุณมีพลังงานไม่พอที่จะทำการวิจัย', 'level': 0}

        if "Union" in str(self.__class__):
            self.experiences += 1
            self.save()
        
        research_result = {'is_success': False, 'formula': None, 'message': 'การวิจัยผิดพลาด', 'level': 0}
        pollution_modifier = 1
        
        # Bad algorightm :(
        for formula in Formula.objects.all():
            if formula.is_match([ownership.item for ownership in ownerships]):                                
                if catalyst is None:
                    modifier = 1
                    pollution_modifier = 1
                elif catalyst.item.name == u'การรีไซเคิล':
                    modifier = 1
                    pollution_modifier = 0.67
                elif catalyst.item.name == u'เครื่องแยกขยะ':
                    modifier = 1
                    pollution_modifier = 0.15
                else:
                    modifier = float(catalyst.research_modifier)/100.0
                    pollution_modifier = 1
                results = Result.objects.filter(formula=formula)
                
                total_storage_costs = 0
                for result in results:
                    total_storage_costs += result.item.storage_cost * result.quantity * modifier
                if self.get_free_space() < total_storage_costs:
                    research_result = {'is_success': True, 'formula': formula, 'message': 'ที่เก็บของไม่พอ', 'license_fee': formula.patent.copy_cost, 'level': 0}
                    break
                    
                if formula.patent.get_owner() != None:
                    if self.money < formula.patent.copy_cost:
                        research_result = {'is_success': True, 'formula': formula, 'message': 'เงินค่าลิกขสิทธ์ไม่พอ', 'license_fee': formula.patent.copy_cost, 'level': 0}
                        break
                    else:
                        self.money -= formula.patent.copy_cost
                        self.save()
                        owner = formula.patent.get_owner()
                        owner.money += formula.patent.copy_cost
                        owner.save()
                
                if formula.patent.status == 2:
                    modifier *= 2
                elif formula.patent.get_owner() == self:
                    modifier *= 2
                    
                # Add result items
                level = min( [ownership.level for ownership in ownerships] )  #TODO: check min level not include u'เทคโนโลยี'
                
                research_result = {'is_success': True, 'formula': formula, 'message': 'วิจัยสำเร็จ', 'license_fee': formula.patent.copy_cost, 'level': level}
    
                for result in results:
                    item_types = result.item.item_types.all()
                    if u'เทคโนโลยี' in [item_type.name for item_type in item_types]:
                        if result.item not in self.items.all():
                            self.add_item(result.item, level)
                        else:
                            ownership = Ownership.objects.get(player=self, item=result.item)
                            if ownership.level < level:
                                ownership.delete()
                                self.add_item(result.item, level)
                            
                    else:
                        #ownerships = list()   #koon debug here
                        
                        for i in range(int(result.quantity * modifier)):
                            # ownership = self.add_item(result.item, level)
                            self.add_item(result.item, level)
                
                break
            # else:
            #     # Debugging
            #     items = [ownership.item for ownership in ownerships]
            #     for item in items:
            #         print item.id,
            #     print
                
                        
        # Decrease durability
        for ownership in ownerships:
            ownership.item.create_pollutions(pollution_modifier)
            if not (u'เทคโนโลยี' in [item_type.name for item_type in ownership.item.item_types.all()]):
                if ownership.durability != None:
                    ownership.durability -= 1       #koon debug
                    if ownership.durability<=0:
                        ownership.delete()
                    else:
                        ownership.save()

        return research_result
        
    def add_item(self, item, level=1):
        """docstring for add_item"""
        if self.get_free_space() < item.storage_cost:
            return False
        
        if u'เทคโนโลยี' not in [item_type.name for item_type in item.item_types.all()]:
            # if item not in self.known_items.all():
            self.known_items.add(item)
        
        ownership = Ownership.objects.create(
            item = item,
            level = level,
            durability = item.durability,
        )
        ownership.set_owner(self)
        
        if item.expiration is not None:
            ownership.expire_at = datetime.now() + timedelta(seconds=item.expiration)
            ownership.save()            #Koon add this line
            
        return ownership
            
    def replenish_energy(self, energy):
        replenished_energy = self.energy + energy
        max_energy = self.get_max_energy()
        if replenished_energy < 0:
            return False
        else:
            if replenished_energy > max_energy:
                replenished_energy = max_energy
            self.energy = replenished_energy
            self.save()              #Koon add this line
            return True
            
    def replenish_mechanical_energy(self, mechanical_energy):
        replenished_mechanical_energy = self.mechanical_energy + mechanical_energy
        max_mechanical_energy = self.get_max_mechanical_energy()
        if replenished_mechanical_energy < 0:
            return False
        else:
            if replenished_mechanical_energy > max_mechanical_energy:
                replenished_mechanical_energy = max_mechanical_energy
            self.mechanical_energy = replenished_mechanical_energy
            self.save()               #Koon add this line
            return True
        
    def get_research_cost(self):
        """docstring for get_research_cost"""
        research_cost = self.research_cost
        for item in self.items.all():
            research_cost += item.research_cost_modifier
        research_cost += int( ServerStatus.objects.get(name='research_cost_modifier').value )
        
        
        for value in [ eval(activeeffect.value) for activeeffect in self.activeeffect_set.all()]:
            if value.has_key('research_cost'):
                research_cost += value['research_cost']
        
        if research_cost < 1:
            research_cost = 1
        return research_cost
        
    def get_regeneration_rate(self):
        """docstring for get_regeneration_rate"""
        regeneration_rate = self.regeneration_rate
        for item in self.items.all():
            regeneration_rate += item.regeneration_rate_modifier
        
        for value in [ eval(activeeffect.value) for activeeffect in self.activeeffect_set.all()]:
            if value.has_key('regeneration_rate'):
                regeneration_rate += value['regeneration_rate']
                
        return regeneration_rate
        
    def get_max_energy(self):
        """docstring for get_max_energy"""
        max_energy = self.max_energy
        for item in self.items.all():
            max_energy += item.max_energy_modifier
        return max_energy
        
    def get_max_mechanical_energy(self):
        """docstring for get_max_energy"""
        max_mechanical_energy = self.max_mechanical_energy
        for item in self.items.all():
            max_mechanical_energy += item.max_mechanical_energy_modifier
        return max_mechanical_energy
        
    class Meta:
        abstract = True

    def __unicode__(self):
        return u"Entity"
        
class Location(StatusModifier):
    """(Location description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name)

class Union(Entity):
    """(Union description)"""
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    experiences = models.IntegerField(default=0)
    auto_share = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.name)

class Player(Entity):
    """(Player model : User profile model)"""
    user = models.OneToOneField(User, unique=True)
    travel_cost = models.IntegerField()
    harvest_cost = models.IntegerField()
    known_items = models.ManyToManyField(Item, related_name='known_by', blank=True, null=True)
    location = models.ForeignKey(Location)
    last_active = models.DateTimeField(default=datetime.now())
    
    # Geo location
    latitude = models.IntegerField()
    longitude = models.IntegerField()
        
    # Union related
    union = models.ForeignKey(Union, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user.username)
        
    # Geo location format: (latitude, longitude)
    def get_geo_location(self):
        """docstring for get_geo_location"""
        return (self.latitude, self.longitude)
        
    def set_geo_location(self, geo_location):
        """docstring for set_geo_location"""
        self.latitude = geo_location[0]
        self.longitude = geo_location[1]
        self.save()
        
    # Unfinished, need to calculate travel cost
    def travel_to(self, location):
        """docstring for travel_to"""
        if self.location != location:
            if self.replenish_energy(-self.get_travel_cost()):
                self.location = location
                self.save()
        
    def harvest(self, unlocker=None):
        """docstring for harvest"""
        if not self.replenish_energy(-self.get_harvest_cost()):
            return {
                'is_success': False,
                'item': None,
                'message': u'คุณมีพลังงานไม่เพียงพอในการหาทรัพยากร',
                'level': 0,
            }
        else:
            location = self.location
            items = list()
            sum_freq = 0
            for harvestible in self.get_harvestibles(unlocker):
                rarity = Rarity.objects.filter(item=harvestible, location=location)
                if list(rarity) != list():
                    item = dict()
                    item['item'] = harvestible
                    tmp=sum_freq +rarity[0].chance
                    item['chance'] = (sum_freq,tmp)
                    sum_freq = tmp
                    items.append(item)
                    
            response = {
                'is_success': False,
                'item': None,
                'message': u'คุณไม่สามารถใช้ไอเทมนี้หาทรัพยากรที่นี่ได้',
                'level': 0,
            }
            
            if items != list():
                chance = randint(1, sum_freq)
                for item in items:
                    if chance > item['chance'][0] and chance<=item['chance'][1]:
                        response['item'] = item['item']
                        break
                
                level = randint(1, 100)
                if level < 50:
                    level = 1
                elif level < 75:
                    level = 2
                elif level < 87:
                    level = 3
                elif level < 93:
                    level = 4
                else:
                    level = 5
                response['item']=self.add_item( response['item'], level )
                if response['item']:
                    response['is_success'] = True
                    response['message'] = ''
                    response['level'] = level
                else:
                    response['message'] = u'คุณเหลือพื้นที่ไม่พอสำหรับไอเทมนี้'
                    response['level'] = 0
                    response['is_success'] = False
                
            return response
        
    # status getter, unfinished        
    def get_travel_cost(self):
        """docstring for get_travel_cost"""
        travel_cost = self.travel_cost
        for item in self.items.all():
            travel_cost += item.travel_cost_modifier
        travel_cost += int( ServerStatus.objects.get(name='travel_cost_modifier').value )
        
        for value in [ eval(activeeffect.value) for activeeffect in self.activeeffect_set.all()]:
            if value.has_key('travel_cost'):
                travel_cost += value['travel_cost']
                
        if travel_cost < 1:
            travel_cost = 1
            
        return travel_cost
        
    def get_harvest_cost(self):
        """docstring for get_harvest_cost"""
        harvest_cost = self.harvest_cost
        for item in self.items.all():
            harvest_cost += item.harvest_cost_modifier
        harvest_cost += int( ServerStatus.objects.get(name='harvest_cost_modifier').value )
        
        for value in [ eval(activeeffect.value) for activeeffect in self.activeeffect_set.all()]:
            if value.has_key('harvest_cost'):
                harvest_cost += value['harvest_cost']
        
        if harvest_cost < 1:
            harvest_cost = 1
        return harvest_cost
        
    def get_harvestibles(self, unlocker=None):
    	"""docstring for get_harvestibles"""
    	harvestibles = set()
    	if unlocker is None:
        	for item in self.items.all():
        	    harvesting = Harvesting.objects.filter(unlocker=item)
        	    if list(harvesting) != list():
        		    harvestibles = set.union(harvestibles, set(harvesting[0].resources.all()))
    	else:
    	    harvesting = Harvesting.objects.filter(unlocker=unlocker)
    	    if list(harvesting) != list():
    		    harvestibles = set(harvesting[0].resources.all())
    	return list(harvestibles)
        
    @staticmethod
    def register(username, password, email, geo_location, is_staff=False):
        """
        Register new user and return new player object
        
        >>> Player.register(username="knightbaron", password="qwerty", email="foo@bar.com", geo_location=(10,-10))
        <Player: knightbaron>
        """
        # Default statues
        DEFAULT_MONEY = 10000
        DEFAULT_LOCATION = Location.objects.get(name='Home')
        DEFAULT_STORAGE = 250
        DEFAULT_MAX_ENERGY = 5000
        DEFAULT_MAX_MECHANICAL_ENERGY = 1000
        DEFAULT_RESEARCH_COST = 100
        DEFAULT_TRAVEL_COST = 40
        DEFAULT_REGENERATION_RATE = 220
        DEFAULT_HARVEST_COST = 60
        
        # Create new user
        user = User.objects.create_user(username, email, password)
        user.is_staff = is_staff
        
        # Save changes to database
        user.save()
        
        try:
            # Create new player, associated with newly created user
            player = Player(user=user,
                money=DEFAULT_MONEY,
                location=DEFAULT_LOCATION,
                storage=DEFAULT_STORAGE,
                energy=DEFAULT_MAX_ENERGY,
                max_energy=DEFAULT_MAX_ENERGY,
                mechanical_energy=0,
                max_mechanical_energy=DEFAULT_MAX_MECHANICAL_ENERGY,
                research_cost=DEFAULT_RESEARCH_COST,
                regeneration_rate=DEFAULT_REGENERATION_RATE,
                travel_cost=DEFAULT_TRAVEL_COST,
                harvest_cost=DEFAULT_HARVEST_COST,
                latitude=geo_location[0],
                longitude=geo_location[1])
            
            # Save new player
            player.save()
        except Exception:
            user.delete()
            raise
        
        return player

class Ownership(models.Model):
    """Abstract models for Player and Union items ownership"""
    item = models.ForeignKey(Item)
    player = models.ForeignKey(Player, blank=True, null=True)
    union = models.ForeignKey(Union, blank=True, null=True)
    level = models.IntegerField(default=1)
    durability = models.IntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    
    def get_owner(self):
        if self.player is not None:
            return self.player
        else:
            return self.union

    def set_owner(self,person):
        if type(person)==Player:
            self.player=person
            self.union=None
        else:
            self.union=person
            self.player=None
        self.save()
        
    @staticmethod
    def clear_expired_items():
        """docstring for clear_expired_items"""
        now = datetime.now()
        for ownership in Ownership.objects.all():
            if ownership.expire_at != None:
                if now > ownership.expire_at:
                    ownership.delete()

    #Koon want to use this for debugging
    def __unicode__(self):
        return u"%s, %s, %s" % (self.id, self.item.name, self.get_owner())

#    def __unicode__(self):
#        return u"Ownership"

#
# Researching, Harvesting related models
#
        
class Formula(models.Model):
    """(Formula description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    components = models.ManyToManyField(Item, related_name='component_for', blank=True, null=True)
    component_types = models.ManyToManyField(ItemType, blank=True, null=True)
    weather = models.ForeignKey(Weather, blank=True, null=True)    
    results = models.ManyToManyField(Item, related_name='created_by', through='Result')
    effects = models.ManyToManyField(Effect, through='Formulas_Effects', blank=True, null=True)
    
    def is_match(self, items): # items is a queryset
        """docstring for is_match"""        
        weather_id = int(ServerStatus.objects.get(name='weather_id').value)
        weather = Weather.objects.get(id=weather_id)      
        if (self.weather != weather and self.weather!=None):
            return False
        
        components = set(self.components.all())
        items = set(items)
            
        if components != set():
            for component in components:
                if component not in items:
                    return False
        
        try:
            from itertools import product
        except Exception:
            # Product method for python 2.5
            def product(*args, **kwds):
                # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
                # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
                pools = map(tuple, args) * kwds.get('repeat', 1)
                result = [[]]
                for pool in pools:
                    result = [x+[y] for x in result for y in pool]
                for prod in result:
                    yield tuple(prod)
        
        items = list( items - components )
                
        combinations = list( product(*[item.item_types.all() for item in items]) )
        
        for i in xrange(len(combinations)):
            combinations[i] = set(combinations[i])
            # combinations[i].sort()
            
        # if components == set():
        #     print 'components:', components
        #     print 'items:', items
        #     print 'items-components:', set(items) - set(components)            
        #     print [ ct.id for ct in self.component_types.all() ]
        #     for combination in combinations:
        #         print [ct.id for ct in combination],
        #     print ''
        
        component_types = set(self.component_types.all())
        # component_types.sort()
        if component_types in combinations:
            return True
        else:
            return False
    
    def get_component(self):
        s=''
        for component in self.components.all():
            s=s+component.name+', '
        for component in self.component_types.all():
            s=s+'('+component.name+'),'
        return s
    
    def get_all_result(self):   #for debug in admin page
        s=''
        for result in Result.objects.filter(formula=self):
            s=s+str(result.quantity)+' '+result.item.name+', '
        return s
        
    def get_results_storage_cost(self):
        """docstring for get_total_storage_cost"""
        storage_cost = 0
        for result in Result.objects.filter(formula=self):
            storage_cost += result.item.storage_cost * result.quantity
        return storage_cost

    def __unicode__(self):
        return unicode(self.name)
        
class Formulas_Effects(models.Model):
    """(Formulas_Effects description)"""
    formula = models.ForeignKey(Formula)
    effect = models.ForeignKey(Effect)
    value = models.TextField(blank=True, null=True)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"Formulas_Effects"


class Result(models.Model):
    """(Results description)"""
    formula = models.ForeignKey(Formula, related_name='result_of')
    item = models.ForeignKey(Item)
    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return u"Results"
        
class Harvesting(models.Model):
    """(Harvesting description)"""
    unlocker = models.OneToOneField(Item, related_name='unlock')
    resources = models.ManyToManyField(Item, related_name='gain_by')
    
    def get_all_item(self):
        s=''
        for item in self.resources.all():
            s=s+item.name+', '
        return s

    def __unicode__(self):
        return u"Harvesting"

class Rarity(models.Model):
    """(Rariry description)"""
    item = models.ForeignKey(Item)
    location = models.ForeignKey(Location)
    chance = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Rarities"

    def __unicode__(self):
        return u"Rariry"

#
# Logging models
#
class Log(models.Model):
    """(Log description)"""
    time = models.DateTimeField(blank=True, default=datetime.now())

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"Log"

class EventLog(Log):
    """(Log description)"""
    EVENT_TYPES = (
        (0, 'Information'),
        (1, 'Error'),
    )
    event_type = models.IntegerField(default=0, choices=EVENT_TYPES)
    message = models.TextField(blank=True)

    def __unicode__(self):
        return u"Log"

class ResearchLog(Log):
    """(ResearchLog description)"""
    player = models.ForeignKey(Player, blank=True, null=True)
    union = models.ForeignKey(Union, blank=True, null=True)
    items = models.ManyToManyField(Item)
    weather = models.ForeignKey(Weather)
    formula = models.ForeignKey(Formula, blank=True, null=True)
    is_success = models.BooleanField(default=False)
    
    def get_owner(self):
        if self.player is not None:
            return self.player
        else:
            return self.union

    def __unicode__(self):
        return u"ResearchLog"

class ActiveEffect(models.Model):
    """(ActiveEffect description)"""
    effect = models.ForeignKey(Effect)
    player = models.ForeignKey(Player, blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    times_left = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"ActiveEffect"
