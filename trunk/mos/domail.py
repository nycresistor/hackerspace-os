import os, random
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = "mos.settings"
sys.path.append("/django/deployment")

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User

from mos.members.models import get_active_members

for user in get_active_members():
#    newpass = ''.join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYZ")] + [random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYZ1234567890%!") for x in range(0,random.choice((7,8)))])

#    user.set_password(newpass)
    user.is_active = True
    user.save()

#    rendered = render_to_string('welcome.mail',{ 
#            'user': user,
#            'newpass': newpass,
#    })

            
    print user, user.email

#    send_mail('Hackerspace.OS Zugangsdaten fuer %s %s' % (user.first_name, user.last_name), rendered, 'Metalab OS Team <mos@lists.metalab.at>', [user.email], fail_silently=False)
