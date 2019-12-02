# TODO: Don't forget to comment out static media serving in production site
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Import MEDIA_ROOT to serve in development
from newtype.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = patterns('',
    # Example:
    # (r'^newtype/', include('newtype.foo.urls')),
    (r'^$', 'newtype.front.views.front'),
    (r'^user/register/$', 'newtype.front.views.register'),
    (r'^main/$', 'newtype.core.views.main'),
    (r'^overview/$', 'newtype.front.views.overview'),
    (r'^cron/$', 'newtype.core.views.cron'),
    (r'^server_status/$', 'newtype.core.views.server_status'),
    (r'^weather/$', 'newtype.core.views.weather'),
    (r'^testmail/', 'newtype.mail.views.testmail'),
    (r'^testpost/', 'newtype.mail.views.testlist'),
    
    # Forward to apps
    (r'^user/', include('newtype.core.urls')),
    (r'^front/', include('newtype.front.urls')),
    (r'^market/', include('newtype.market.urls')),
    (r'^mail/', include('newtype.mail.urls')),
    (r'^patent/', include('newtype.patent.urls')),
	(r'^core_union/', include('newtype.core_union.urls')),
	(r'^hof/', include('newtype.hall_of_fame.urls')),
	(r'^help/', include('newtype.help.urls')),
	(r'^chart/', include('newtype.chart.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Serving media for testing purpose    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': MEDIA_ROOT}),

    # HACKS
    ('^forum/', 'django.views.generic.simple.redirect_to', {'url': 'http://localhost/forum'}),
    
)
