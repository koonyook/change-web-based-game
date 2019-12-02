# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^newtype/', include('newtype.foo.urls')),
    (r'^login/$', 'newtype.core.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^location/$', 'newtype.core.views.location'),
    (r'^items/$', 'newtype.core.views.items'),
    (r'^status/$', 'newtype.core.views.status'),
    (r'^research_log/$', 'newtype.core.views.research_log'),
    (r'^menu/$', 'newtype.core.views.menu'),
    (r'^use_item/$', 'newtype.core.views.use_item'),        #Koon debug this line
    (r'^remove_item/$', 'newtype.core.views.remove_item'),  #Koon add this line
    (r'^research/$', 'newtype.core.views.research'),
    (r'^harvest/$', 'newtype.core.views.harvest'),
    (r'^state/$', 'newtype.core.views.state'),
)
