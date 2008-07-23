import datetime
import locale

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink, Q


locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return u"%s" % self.name
    

class Location(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return u"%s" % self.name


class EventManager(models.Manager):
    def get_query_set(self):
        return super(EventManager, self).get_query_set().filter(deleted=False)

class FutureEventFixedNumberManager(EventManager):
    def get_query_set(self):
        """ Get <num> future events, or if there aren't enough, get <num> latest+future events. """

        DEFAULT_NUM = 5
        if(hasattr(settings,'HOS_HOME_EVENT_NUM')):
            num = settings.HOS_HOME_EVENT_NUM
        else:
            num = DEFAULT_NUM

        all = super(FutureEventFixedNumberManager,self).get_query_set().order_by('startDate')
        future = all.filter(
                            (Q(endDate__gte=datetime.datetime.now())) |
                            (Q(endDate__isnull=True) & Q(startDate__gte=datetime.datetime.now()-datetime.timedelta(hours=5)))).order_by('startDate') # event visible 5 hours after it started

        if(future.count()<num):
            if(all.count()-num>=0):
                latest = all[all.count()-num:all.count()]
            else:
                latest = all
        else:
            latest = future[:num]

        return latest

class Event(models.Model):
    name = models.CharField(max_length=200)
    teaser = models.TextField(max_length=200, blank=True, null=True)
    wikiPage = models.CharField(max_length=200)
        
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(blank=True, null=True)
    
    who = models.CharField(max_length=200,blank=True)
    where = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(default=datetime.datetime.now())
    created_by = models.ForeignKey(User)

    deleted = models.BooleanField(default=False)

    category = models.ForeignKey(Category, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    objects = models.Manager()
    all = EventManager()
    future = FutureEventFixedNumberManager()
        
    def __unicode__(self):
        status = ''
        if self.deleted:
            status = ' [deleted]' 
        return u'%s (%s)%s' % (self.name, self.startDate, status)
        
    def past(self):
        return self.startDate < datetime.datetime.now() 

    @permalink
    def get_absolute_url(self):
        return('django.views.generic.list_detail.object_detail', [str(self.id)])
        
    def save(self, editor=False, new=False):
        if new and editor != False :
            self.created_by = editor
            self.created_by.save()
           
        super(Event, self).save()
            
    def start_end_date_eq(self):
        return self.startDate.date() == self.endDate.date()

