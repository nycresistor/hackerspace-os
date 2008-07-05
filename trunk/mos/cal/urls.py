from django.conf.urls.defaults import *
from mos import settings

from models import Event
from forms import EventForm
import datetime

date_dict = {
    'queryset': Event.all.all(),
    'date_field': 'startDate',
    'allow_future': True,
    'allow_empty': True,
    'num_latest': 100,
    'template_object_name': 'latestevents',
}

info_dict = {
    'queryset': Event.all.all(),
    'template_object_name': 'event',
}

urlpatterns = patterns('django.views.generic.date_based',
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', date_dict),
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',               'archive_day',   date_dict),
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',                                'archive_month', date_dict),
#   (r'^(?P<year>\d{4})/$',                                                    'archive_year',  date_dict),
   (r'^$',                                                                    'archive_index', date_dict),
)

urlpatterns += patterns('',
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    (r'^(?P<object_id>\d+)/update/$', 'mos.cal.views.update_event', {'new': False}),
    (r'^(?P<object_id>\d+)/delete/$', 'mos.cal.views.delete_event'),
    (r'^new/$', 'mos.cal.views.update_event', {'new': True}),    
)
