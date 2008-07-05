from django.conf.urls.defaults import *
from mos import settings
from mos.members.models import *
from django.contrib.auth.models import User
import datetime
import django.views.generic.list_detail
from django.db.models import Q


info_dict = {
    'queryset': get_active_members()
#	'queryset': User.objects.filter(
#                                    Q(membershipperiod__begin__lte=datetime.datetime.now()),
#                                    Q(membershipperiod__end__isnull=True) | Q(membershipperiod__end__gte=datetime.datetime.now()) 
#                                ).distinct(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^history/$', 'mos.members.views.members_history'),
    (r'^change_password/$', 'django.contrib.auth.views.password_change'),
    (r'^change_password/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^collection/$', 'mos.members.views.members_bankcollection_list'),
    (r'^(?P<user_username>\w+)/$', 'mos.members.views.members_details'), #this should be a generic view in version2
    (r'^(?P<user_username>\w+)/update/(?P<type>\w+)/$', 'mos.members.views.members_update'), #this should be a generic view in version2

)
