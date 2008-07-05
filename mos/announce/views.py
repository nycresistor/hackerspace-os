#
# Views for issueing announcements to all active members.
#
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django import newforms as forms
from mos.members.models import get_active_members, ContactInfo
from django.core.mail import send_mail
import smtplib


class AnnouncementForm(forms.Form):
    subject = forms.CharField(required=True, label="Thema", max_length=40)
    body    = forms.CharField(required=True, label="Mitteilung",
                              widget=forms.Textarea)


@user_passes_test(lambda u: (u.is_staff and u.is_authenticated()))
def announce(request):
    print 'wtf:' + repr(request.user)
    form = AnnouncementForm(request.POST or None)
    if not request.POST or not form.is_valid():
        return render_to_response('announce/write_message.html',
                                  {
                                   'form': form,
                                   'user': request.user,
                                  })
    # Valid message: send it!
    s = ''
    for user in get_active_members():
        ci = ContactInfo.objects.get(user=user)
        try:
            send_mail(form.cleaned_data['subject'],
                      form.cleaned_data['body'],
                      settings.ANNOUNCE_FROM,
                      [user.email],
                      fail_silently=False)
            ci.last_email_ok = True
            ci.save()
        except smtplib.SMTPException, instance:
             f = open('/announcelog.log','a')
             f.write('\n\n'+user.email)
             f.write('\n'+repr(instance))
             ci.last_email_ok = False
             ci.save()
             f.close()

    return render_to_response('announce/message_sent.html',
                              {
                               'form': form,
                               'user': request.user,
                               })

