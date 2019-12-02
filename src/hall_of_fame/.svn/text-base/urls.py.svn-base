# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('newtype',
    # Example:
    # (r'^newtype/', include('newtype.foo.urls')),
    (r'^players_max_money/(?P<limit>\d+)/$', 'hall_of_fame.views.players_max_money'),
    (r'^players_most_research/(?P<limit>\d+)/$', 'hall_of_fame.views.players_most_research'),
    (r'^players_most_found_patent/(?P<limit>\d+)/$', 'hall_of_fame.views.players_most_found_patent'),
    (r'^players_most_regis_patent/(?P<limit>\d+)/$', 'hall_of_fame.views.players_most_regis_patent'),
    (r'^unions_max_money/(?P<limit>\d+)/$', 'hall_of_fame.views.unions_max_money'),
    (r'^unions_most_research/(?P<limit>\d+)/$', 'hall_of_fame.views.unions_most_research'),
    (r'^unions_most_regis_patent/(?P<limit>\d+)/$', 'hall_of_fame.views.unions_most_regis_patent'),
)
