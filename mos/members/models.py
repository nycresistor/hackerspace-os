from django.db import models
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q

class PaymentInfo(models.Model):
    bank_collection_allowed = models.BooleanField()
    bank_collection_mode = models.ForeignKey('BankCollectionMode', core=True)
    bank_account_owner = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_code = models.CharField(max_length=20, blank=True)
    
    user = models.ForeignKey(User, unique=True, edit_inline=models.STACKED, min_num_in_admin=0, num_in_admin=1, max_num_in_admin=1)

class ContactInfo(models.Model):
    on_intern_list = models.BooleanField(default=True, core=True)
    intern_list_email = models.EmailField(blank=True)
    
    street = models.CharField(max_length=200)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    phone_number = models.CharField(max_length=32, blank=True)
    birthday = models.DateField(null=True, blank=True)

    wiki_name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='userpics', blank=True)

    user = models.ForeignKey(User, unique=True, edit_inline=models.STACKED, num_in_admin=1, max_num_in_admin=1)


    last_email_ok = models.BooleanField(null=True)
    
    def get_debts(self):
        #FIXME: this is broken because it assumes that a membership period
        #       has a constant fee
        arrears = 0
        mp_list = MembershipPeriod.objects.filter(user=self.user)
        for mp in mp_list:
            fee = MembershipFee.objects.get(kind_of_membership=mp.kind_of_membership)
            if fee.amount > 0:
                arrears += mp.get_duration_in_month()*fee.amount
        return arrears - self.get_all_payments()


    def get_debt_for_month(self, date_in_month):
        #see if the there is a membership period for the month
        mp_list = MembershipPeriod.objects.filter(user=self.user).filter(
                    Q(begin__lte=date_in_month),
                    Q(end__isnull=True) | Q(end__gte=date_in_month))

        if mp_list.count() == 0:
            return 0
        else:
            #find the membership fee for the month and kind of membership and return amount
            mp = mp_list[0]
            fee = mp.kind_of_membership.membershipfee_set.filter(
                Q(start__lte=date_in_month),
                Q(end__isnull=True) | Q(end__gte=date_in_month))[0]

            return fee.amount
            
        
    def get_all_payments(self):
        payments = 0
        p_list = Payment.objects.filter(user=self.user)
        for p in p_list:
            payments += p.amount
        return payments
    
    def get_date_of_entry(self):
        mp = MembershipPeriod.objects.filter(user=self.user).order_by('-begin')[0]
        return mp.begin
        
    def get_current_membership_period(self):
        mp = MembershipPeriod.objcts.filter(user=self.user).order_by('begin')[0]
        if mp.end is None:
            return mp
        else:
            return None
        return mp.begin
    
    def get_wikilink(self):
        if self.wiki_name==None:
            return None
        else:
            return u'%s/Benutzer:%s' % (settings.WIKI_URL, self.wiki_name)

def get_active_members():
    return User.objects.filter(
                Q(membershipperiod__begin__lte=datetime.datetime.now()),
                Q(membershipperiod__end__isnull=True) | Q(membershipperiod__end__gte=datetime.datetime.now())
              ).distinct()

class BankCollectionMode(models.Model):
    name = models.CharField(max_length=20)
    num_month = models.IntegerField()
    
    def __unicode__(self):
        return u"%s" % self.name

class MembershipPeriod(models.Model):
    begin = models.DateField(core=True)
    end = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, edit_inline=models.TABULAR, num_in_admin=1 )
    kind_of_membership = models.ForeignKey('KindOfMembership')
    class Admin:
        list_display = ('user', 'begin', 'end', 'kind_of_membership')
    
    def __unicode__(self):
        return u"%s" % self.user.username
        
    def get_duration_in_month(self):
        if self.end is None :
            end = datetime.date.today()
        else:
            end = self.end
        if end < self.begin :
            return 0
        
        begin = datetime.date(self.begin.year, self.begin.month, 1)
        end = datetime.date(end.year, end.month, 2)
        
        month = 0
        while begin < end :
            if begin.month == 12 :
                begin = datetime.date(begin.year + 1, 1, 1)
            else :
                begin = datetime.date(begin.year, begin.month + 1, 1)
            month += 1
        return month
    
class MembershipFee(models.Model):
    '''
    Defines the membership fee for a certain period of time.
    With this class it is possible to define different amount of
    membership fees for different periods of time and for different
    kind of members, e.g. pupils, unemployees, normal members, ...
    '''
    kind_of_membership = models.ForeignKey('KindOfMembership')
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    amount = models.IntegerField()
    
    def __unicode__(self):
        return u"%s - %d" % (self.kind_of_membership, self.amount)

class KindOfMembership(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.name
    
class Payment(models.Model):
    amount = models.FloatField()
    comment = models.CharField(max_length=200)
    date = models.DateField()
    method = models.ForeignKey('PaymentMethod')
    user = models.ForeignKey(User)
      
    def __unicode__(self):
        return u"%s" % self.user.username

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
      
    def __unicode__(self):
        return u"%s" % self.name
