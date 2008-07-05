import datetime
import time

from django.template import loader, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.xheaders import populate_xheaders
from django.db.models.fields import DateTimeField
from django.http import Http404, HttpResponse
import django.views.generic.date_based

def archive_index_prefer_future(request, queryset, date_field, num_latest=15,
        template_name=None, template_loader=loader,
        extra_context=None, allow_empty=True, context_processors=None,
        mimetype=None, template_object_name='latest'):
    """
    Generic top-level archive of date-based objects.

    Templates: ``<app_label>/<model_name>_archive.html``
    Context:
        date_list
            List of years
        latest
            Latest N (defaults to 15) objects by date
    """
    if extra_context is None: extra_context = {}
    model = queryset.model
    elements = queryset.filter(**{'%s__gte' % date_field: datetime.datetime.now()}).order_by(date_field)
    if elements.count()<=num_latest:
        return django.views.generic.date_based.archive_index(request,queryset,date_field,num_latest=num_latest,template_name=template_name,
                template_loader=template_loader,extra_context=extra_context,allow_empty=allow_empty,context_processors=context_processors,
                mimetype=mimetype,template_object_name=template_object_name,allow_future=True)
    else:
        elements = elements.order_by("-"+date_field)[0:num_latest]
    queryset = elements

    latest = queryset

    if not template_name:
        template_name = "%s/%s_archive.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        template_object_name : latest,
    }, context_processors)
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    return HttpResponse(t.render(c), mimetype=mimetype)
