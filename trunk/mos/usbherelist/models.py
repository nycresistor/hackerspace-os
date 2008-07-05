from django.db import models

# Create your models here.

class Usbhereitem:
    def __init__(self,nick=""):
        self.nick = nick

    def __str__(self):
       	return "%s" % (self.nick)
#return self.__unicode__()

    def __unicode__(self):
        return "%s" % (self.nick)
