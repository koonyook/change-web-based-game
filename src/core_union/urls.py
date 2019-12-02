# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('newtype.core_union.views',
    # Example:
    # (r'^newtype/', include('newtype.foo.urls')),
    (r'^show_topic/$', 'show_topic'),
	(r'^read_topic/$', 'read_topic'),
	(r'^new_topic/$', 'new_topic'),
	(r'^reply_topic/$', 'reply_topic'),
	(r'^delete_topic/$', 'delete_topic'),

	(r'^show_setting/$', 'show_setting'),
	(r'^set_setting/$', 'set_setting'),
	(r'^delete_member/$', 'delete_member'),
	(r'^transfer_item/$', 'transfer_item'),
	(r'^transfer_money/$', 'transfer_money'),

	(r'^get_open_cost/$', 'get_open_cost'),
	(r'^new_union/$', 'new_union'),
)
