# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.html import escape

from newtype.core.models import Player,Union
import datetime
# Create your models here.

class Forum(models.Model):
	union = models.ForeignKey(Union)
	player = models.ForeignKey(Player)
	subject = models.CharField(max_length=255)

	def __unicode__(self):
		return unicode(self.union)+': '+unicode(self.subject)

class Reply(models.Model):
	forum = models.ForeignKey(Forum)
	player = models.ForeignKey(Player)
	reply_at = models.DateTimeField(default=datetime.datetime.now())
	message = models.TextField()

	def __unicode__(self):
		return unicode(self.player)+': '+unicode(self.message)

class SettingUnion(models.Model):
	player = models.OneToOneField(Player, unique=True)
	can_research	= models.BooleanField(default=False)
	can_transfer_item	= models.BooleanField(default=False)
	can_take_money	= models.BooleanField(default=False)
	can_persuade	= models.BooleanField(default=False)
	can_set			= models.BooleanField(default=False)
	share_rate		= models.IntegerField(default=0, blank=True, null=True)
	rank			= models.IntegerField(blank=True, null=True)			#1=head

	def __unicode__(self):
		return u'SettingUnion'