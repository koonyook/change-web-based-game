# -*- coding: UTF-8 -*-
import datetime

def trim_time(this_time):
	if type(this_time)==datetime.datetime:
		return unicode(this_time-datetime.timedelta(microseconds=this_time.microsecond))
	else:
		return unicode(this_time)