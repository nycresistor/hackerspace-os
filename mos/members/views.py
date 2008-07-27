from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


from datetime import *
from dateutil.rrule import *

from mos.members.models import *
from mos.members.util import *
from mos.members.forms import UserEmailForm, UserNameForm, UserAdressForm

import sys

@login_required
def members_history(request):
    history_entry_list = get_list_of_history_entries()
    history_list = []
    months = list( rrule(MONTHLY, dtstart=date(2006, 3, 1), until=date.today()) )
    for dt in months:
        history_list.append(history_entry_list[dt.date()])
    history_list.reverse()
    return render_to_response('members/members_history.html', {'list': history_list}, context_instance=RequestContext(request))

def members_details(request, user_username, errors="", update_type=""):
    editable = False
    if request.user.username == user_username :    
        editable = True
    user = get_object_or_404(User, username = user_username)
    return render_to_response('members/members_details.html', {'item': user, 
                                                               'ea' : editable, 
                                                               'error_form' : errors,
                                                               'error_type' : update_type
                                                               }, 
                              context_instance=RequestContext(request))

def members_update(request,user_username, update_type):
    if not request.POST or not request.user.username == user_username :
        return members_details(request, user_username, "no permission to edit settings")
    user = get_object_or_404(User, username = user_username)    

    error_form = False
    error_type = False

    if update_type == "email" and request.method == "POST":
        update_form = UserEmailForm(request.POST, instance=user)
    elif update_type == "name" and request.method == "POST" :
        update_form = UserNameForm(request.POST,instance=user)
    elif update_type == "adress" and request.method == "POST":
        contact_info = get_object_or_404(ContactInfo, user=user)
        update_form = UserAdressForm(request.POST, instance=contact_info)
    
    if update_form.is_valid():
        update_form.save()
    else:
        error_form = update_form
        error_type = update_type

    return members_details(request, user_username, error_form,error_type)

@login_required
def members_bankcollection_list(request):
    if request.user.is_superuser:
        #get members that are active and have monthly collection activated
        members_to_collect_from = get_active_members().filter(paymentinfo__bank_collection_allowed=True) \
                                    .filter(paymentinfo__bank_collection_mode__id = 4) # 4 = monthly


        #build a list of collection records with name, bank data, amount and a description
        collection_records = []

        for m in members_to_collect_from:
            debt = m.contactinfo_set.all()[0].get_debt_for_month(date.today())
            if debt != 0:
                pmi = m.paymentinfo_set.all()[0]
                ci = m.contactinfo_set.all()[0]
                collection_records.append([m.first_name, m.last_name, pmi.bank_account_number, pmi.bank_code, pmi.bank_account_owner, str(debt), 'Mitgliedsbeitrag %d/%d;'%(date.today().year,date.today().month)])

        #format as csv and return it
        csv = '\r\n'.join([';'.join(x) for x in collection_records])

        return HttpResponse(csv, mimetype='text/plain')


    else:
        return HttpResponseNotAllowed('you are not allowed to use this method')

