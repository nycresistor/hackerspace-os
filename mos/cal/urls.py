from django.conf.urls.defaults import *

from mos.cal.models import Event, Location, Category
from mos.core.context_processors import calendar_context


date_dict = {
    'queryset': Event.all.all(),
    'date_field': 'startDate',
    'allow_future': True,
    'allow_empty': True,
    'num_latest': 100,
    'template_object_name': 'latestevents',
    'context_processors': [calendar_context],
}

info_dict = {
    'queryset': Event.all.all(),
    'template_object_name': 'event',
}

info_dict_locations = {
    'queryset': Location.objects.all(),
 #   'template_object_name': 'locations',
    'template_name': 'cal/event_locations.html',
   'context_processors': [calendar_context],
}

info_dict_categories = {
    'queryset': Category.objects.all(),
 #   'template_object_name': 'locations',
    'template_name': 'cal/event_categories.html',
   'context_processors': [calendar_context],
}


urlpatterns = patterns('django.views.generic.date_based',
  (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
   'object_detail', date_dict),
  (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
   'archive_day', date_dict),
  (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
   'archive_month', date_dict),
  (r'^(?P<year>\d{4})/$',
   'archive_year', date_dict),
  (r'^$',
   'archive_index', date_dict),
)

urlpatterns += patterns('',
    (r'^special/(?P<typ>\w+)/(?P<name>\w+)/$',
     'mos.cal.views.display_special_events'),
    (r'^(?P<object_id>\d+)/$',
     'django.views.generic.list_detail.object_detail', info_dict),
    (r'^(?P<object_id>\d+)/update/$',
     'mos.cal.views.update_event', {'new': False}),
    (r'^(?P<object_id>\d+)/delete/(?P<came_from>\w+)/',
     'mos.cal.views.delete_event'),
    (r'^new/$', 'mos.cal.views.update_event', {'new': True}),
    (r'^locations/$',
     'django.views.generic.list_detail.object_list', info_dict_locations),
    (r'^categories/$',
     'django.views.generic.list_detail.object_list', info_dict_categories),
    (r'^ajax/list/(?P<number>\d*)/?$', 'mos.cal.views.list'),
)
