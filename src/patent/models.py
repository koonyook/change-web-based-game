# -*- coding: UTF-8 -*-
from django.db import models
from newtype.core.models import Player,Union,Formula
# Create your models here.
import datetime

class Patent(models.Model):
	STATUS_CHOICE = (
		(0,u'ยังไม่ถูกจดทะเบียน'),
		(1,u'สิทธิบัตรจดทะเบียนถูกต้อง'),
		(2,u'สิทธิบัตรสาธารณะ'),
		(3,u'Obsolesce'),
	)
	formula = models.OneToOneField(Formula , unique=True)
	status = models.IntegerField(choices=STATUS_CHOICE , default=0)
	player = models.ForeignKey(Player, related_name='patent_regis', blank=True, null=True)
	union  = models.ForeignKey(Union , related_name='patent_regis', blank=True, null=True)
	
	founder = models.ForeignKey(Player, related_name='patent_found', blank=True, null=True)		#first player who found this formula
	found_at = models.DateTimeField(blank=True, null=True)

	regis_at = models.DateTimeField(blank=True, null=True)
	regis_cost = models.IntegerField(blank=True, null=True, default=100)
	copy_cost = models.IntegerField(blank=True, null=True, default=1)

	is_available = models.BooleanField(default=True)

	def get_owner(self):
		if self.player != None:
			return self.player
		elif self.union != None:
			return self.union
		else:
			return None

	def set_owner(self,person):
		if type(person)==Player:
			self.player=person
			self.union=None
		elif type(person)==Union:
			self.union=person
			self.player=None
		elif person==None:
			self.union=None
			self.player=None
		self.save()

	def set_founder(self,player):
		if self.founder==None and type(player)==Player:
			self.founder=player
			self.found_at=datetime.datetime.now()
			self.save()
			return True
		else:
			return False

	def __unicode__(self):
		return unicode(self.formula.name)