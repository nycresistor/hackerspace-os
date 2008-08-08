# Create your views here.
from dateutil.parser import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from mos.cal.forms import EventForm
from mos.cal.models import Event, Category, Location


def display_special_events(request, typ, name):
    """
    Displays special events by location or category
    """

    try:
        if typ == 'Category':
            events = Event.objects.filter(category__name=name)
            des = get_object_or_404(Category, name=name)
        elif typ == 'Location':
            events = Event.objects.filter(location__name=name)
            des = get_object_or_404(Location, name=name)
        else:
            events = None
            des = None

    except ObjectDoesNotExist:
        events = None

    return render_to_response('cal/event_archive.html', {
                               'latestevents': events,
                               'title': name,
                               'type': typ,
                               'description': des,
                               }, context_instance=RequestContext(request))


@login_required
def delete_event(request, object_id=None, came_from=''):
    if not request.method == 'POST' or not request.user.is_authenticated():
        return

    event = Event.all.get(id=object_id)

    event.delete()
    event.save()

    if came_from == 'calendar':
        latest = Event.all.all().order_by('-startDate')
    else:
        latest = Event.future.all()

    return render_to_response('cal/calendar.inc', {
                'latestevents': latest,
                }, context_instance=RequestContext(request))


@login_required
def update_event(request, new, object_id=None):
    if not request.POST or not request.user.is_authenticated():
        #return
        pass

    if not new:
        event = Event.all.get(id=object_id)
    else:
        event = Event()

    event_error_id = ' '

    event_valid = True

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)

        if event_form.is_valid():
            event_data = event_form.save(commit=False)
            event_data.save(request.user, new)
            event = Event.objects.get(id=event_data.id)
        else:
            print 'lolwhat'
            event_valid = False
            event_error_id = event.id

    else:
        event_form = EventForm()

    response = render_to_response('cal/eventinfo_nf.inc', {
            'event_error_id': event_error_id,
            'event_form': event_form,
            'event': event,
            'new': not event.pk,
            }, context_instance=RequestContext(request))

    if not event_valid:
        response.status_code = 500
        print dir(response)
    return response


def list(request, number=0):
    events = Event.future.get_n(long(number) if number != '' else 0)

    if not number:
        events = events.reverse()

    return render_to_response('cal/calendar.inc',
                              {'latestevents': events},
                              context_instance=RequestContext(request))
