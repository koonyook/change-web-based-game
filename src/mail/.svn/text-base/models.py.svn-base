# -*- coding: UTF-8 -*-
from django.db import models

from newtype.core.models import Item,Player,Union,Ownership
import datetime
# Create your models here.
'''
class Players_Items_Mails(models.Model):
	player_item = models.OneToOneField(Players_Items, unique=True)
	def __unicode__(self):
		return u"%s, %s, %s" % (self.id, self.player_item.item.name, self.player_item.owner)

class Unions_Items_Mails(models.Model):
	union_item = models.OneToOneField(Unions_Items, unique=True)
	def __unicode__(self):
		return u"%s, %s, %s" % (self.id, self.union_item.item.name, self.union_item.owner)
'''
class Mail(models.Model):	
	TYPE_CHOICE = (
		(1,u'basic message & alerting'),
		(2,u'invitation from union'),
		(3,u'gift'),
		(4,u'first step of trade'),
		(5,u'second step of trade'),
	)
	'''
	HUMAN_CHOICE = (
		(u'player',u'player'),
		(u'union',u'union'),
	)
	'''
	type = models.IntegerField(choices=TYPE_CHOICE)
	subject = models.CharField(max_length=255)
	message = models.TextField(blank=True, null=True)
	send_at = models.DateTimeField(default=datetime.datetime.now())			#do not sure

	unread  = models.BooleanField(default=True)
	waiting = models.BooleanField(default=True)

	#send_by = models.CharField(max_length=7, choices=HUMAN_CHOICE)
	send_by_player = models.ForeignKey(Player, related_name='source_mail', blank=True, null=True) 
	send_by_union  = models.ForeignKey(Union , related_name='source_mail', blank=True, null=True)
	
	#send_to = models.CharField(max_length=7, choices=HUMAN_CHOICE)
	send_to_player = models.ForeignKey(Player, related_name='target_mail', blank=True, null=True) 
	send_to_union  = models.ForeignKey(Union , related_name='target_mail', blank=True, null=True)
	
	item1 = models.ManyToManyField(Ownership, related_name='trade1', blank=True, null=True)
	money1 = models.IntegerField(blank=True, null=True)

	item2 = models.ManyToManyField(Ownership, related_name='trade2', blank=True, null=True)
	money2 = models.IntegerField(blank=True, null=True)
	
	def set_sender(self,person):
		if (type(person)==Player):
			self.send_by_player=person
		else:
			self.send_by_union=person
		self.save()
	
	def set_receiver(self,person):
		if (type(person)==Player):
			self.send_to_player=person
		else:
			self.send_to_union=person
		self.save()

	def set_item(self,num,item_list):   #num= 1 or 2  #item_list= list of Players_Items ID or list of Unions_Items ID
		for item_id in item_list:
			item = Ownership.objects.get(id=item_id)
			item.is_available = False
			item.save()
			if (num==1):
				self.item1.add(item)
			else:
				self.item2.add(item)
	
	def get_item_list(self,num):		#num=1,2
		if num==1:
			tmp=self.item1.all().values_list('id')
		else:
			tmp=self.item2.all().values_list('id')
		ans=[]
		for i in range(len(tmp)):
			ans.append(tmp[i][0])
		return ans

	def count_space(self,num):
		if num==1:
			tmp=self.item1.all()
		else:
			tmp=self.item2.all()
		ans=0
		for e in tmp:
			ans+=e.item.storage_cost
		return ans

	def transfer_items(self,num,person):
		if num==1:
			tmp=self.item1.all()
		else:
			tmp=self.item2.all()
		for e in tmp:
			e.is_available=True
			e.set_owner(person)
			e.save()

	def get_sender(self):
		if (self.send_by_player is not None):
			return self.send_by_player
		elif (self.send_by_union is not None):
			return self.send_by_union
		else:
			return None
	
	def get_receiver(self):
		if (self.send_to_player is not None):
			return self.send_to_player
		elif (self.send_to_union is not None):
			return self.send_to_union
		else:
			return None

	def __unicode__(self):
		return unicode(self.subject)