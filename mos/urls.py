from django.conf.urls.defaults import *
from django.contrib import admin

from cal.feeds import EventFeed

import settings

feeds = {
        'events': EventFeed,
        }


# used for 
js_info_dict = {
    		'packages': ('django.conf',),
	       }


urlpatterns = patterns('',
 #   (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),    


    (r'^cal/', include('mos.cal.urls')),
    (r'^rss/', include('mos.rss.urls')),
    
    (r'^project/', include('mos.projects.urls')),

    (r'^$', 'mos.web.views.display_main_page'),
    
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
 
 # doesnt work with recent django
 #  (r'^admin/', include('django.contrib.admin.urls')), 
#    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment this for admin:
    ('^admin/(.*)', admin.site.root),

    (r'^login/?$', 'django.contrib.auth.views.login'),
    (r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page':'/'}),

    (r'^member/', include('mos.members.urls')),
    
    (r'^wiki/.*$', 'mos.web.views.wikipage'),
#    (r'^usbherelist/', include('mos.usbherelist.urls')),

    (r'^announce/$', include('mos.announce.urls'))
)
