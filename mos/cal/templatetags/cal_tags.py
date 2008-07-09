from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from mos.cal.models import Location, Category, Event

register = template.Library()
 
""" MAKE get_category_list and get_location_list generic"""
@register.filter
def get_category_list(value):
    try:
        return Category.objects.all()
    except ObjectDoesNotExist:
        return None

@register.filter
def get_location_list(value):
    try:
        return Location.objects.all()
    except ObjectDoesNotExist:
        return None

@register.filter
def get_events_by_location(value,arg):
    try:
        return Event.objects.filter(location__name=arg).order_by('startDate')[:4]
    except ObjectDoesNotExist:
        return None

@register.filter
def get_events_by_category(value,arg):
    try:
        return Event.objects.filter(category__name=arg).order_by('startDate')[:4]
    except ObjectDoesNotExist:
        return None
#    try : 
#        return ['foo','bar']
#    except  ObjectDoesNotExist:
 #       return 0
    
    
