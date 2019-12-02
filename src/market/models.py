# -*- coding: UTF-8 -*-
from django.db import models
from newtype.core.models import Item,Player,Union,Ownership
from newtype.patent.models import Patent
import datetime
# Create your models here.

class Deal(models.Model):
	price = models.IntegerField()
	expire_at = models.DateTimeField()
	
	class Meta:
		abstract = True

	def __unicode__(self):
		return u"Deal"

class Sell(Deal):
	# price in this class is true price

	item = models.OneToOneField(Ownership , unique=True)

	def cancle(self):
		self.item.is_available=True
		self.item.save()
		self.delete()

	def item_name(self):
		return self.item.item.name
	
	def seller(self):
		return self.item.get_owner()
	
	def item_level(self):
		return self.item.level

	def __unicode__(self):
		return u"%s, %s, %s, %s" % (self.id, self.item.item.name, self.price, self.item.get_owner())

class Buy(Deal):
	# price in this class is full price for a complete item.
	item = models.ForeignKey(Item)
	level = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()
	must_complete = models.BooleanField()
	buyer_player = models.ForeignKey(Player, blank=True, null=True)
	buyer_union = models.ForeignKey(Union, blank=True, null=True)

	def set_buyer(self,person):
		if (type(person)==Player):
			self.buyer_player=person
		else:
			self.buyer_union=person
		self.save()

	def get_buyer(self):
		if (self.buyer_player is not None):
			return self.buyer_player
		elif (self.buyer_union is not None):
			return self.buyer_union
		else:
			return None

	def cancle(self):
		buyer=self.get_buyer()
		get_back=self.price*self.quantity
		buyer.money+=get_back
		buyer.reserve_space-=self.item.storage_cost*self.quantity
		buyer.save()
		self.delete()
		return get_back

	def item_name(self):
		return self.item.name

	def __unicode__(self):
		return u"%s, %s, %s, %s" % (self.id, self.item.name, self.price, self.get_buyer())

class SellPatent(models.Model):
	patent = models.OneToOneField(Patent , unique=True)
	price = models.IntegerField()
	start_at = models.DateTimeField(default=datetime.datetime.now())
	
	def cancle(self):
		self.patent.is_available=True
		self.patent.save()
		self.delete()
	
	def seller(self):
		return self.patent.get_owner()

	def __unicode__(self):
		return u"%s, %s, %s, %s" % (self.id, self.patent.formula.name, self.price, self.patent.get_owner())