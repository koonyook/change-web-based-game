# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.
class QuestionAnswer(models.Model):
	question = models.TextField()
	answer = models.TextField()

	def __unicode__(self):
		return unicode(self.question)