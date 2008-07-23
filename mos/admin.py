from django.contrib import admin
from django.contrib.auth.models import User

from mos.cal.models import Event, Category, Location
from mos.members.models import ContactInfo, KindOfMembership, PaymentInfo, \
                               MembershipFee, MembershipPeriod, Payment, PaymentMethod
from mos.projects.models import Project


calendar_admin = admin.AdminSite()
calendar_admin.register(Event)
calendar_admin.register(Category)
calendar_admin.register(Location)

project_admin = admin.AdminSite()
project_admin.register(Project)

member_admin = admin.AdminSite()
member_admin.register(User)
member_admin.register(ContactInfo)
member_admin.register(KindOfMembership)
member_admin.register(PaymentInfo)
member_admin.register(MembershipFee)
member_admin.register(MembershipPeriod)
member_admin.register(Payment)
member_admin.register(PaymentMethod)

