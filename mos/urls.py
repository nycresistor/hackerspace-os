from django.conf.urls.defaults import *
from cal.feeds import EventFeed

import settings

feeds = {
        'events': EventFeed,
        }

urlpatterns = patterns('',
 #   (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),    


    (r'^cal/', include('mos.cal.urls')),
    (r'^rss/', include('mos.rss.urls')),
    
    (r'^project/', include('mos.projects.urls')),

    (r'^$', 'mos.web.views.display_main_page'),
    
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^login/?$', 'django.contrib.auth.views.login'),
    (r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page':'/'}),

    (r'^member/', include('mos.members.urls')),
    
    (r'^wikipage/.*$', 'mos.web.views.wikipage'),
#    (r'^usbherelist/', include('mos.usbherelist.urls')),

    (r'^announce/$', include('mos.announce.urls'))
)
