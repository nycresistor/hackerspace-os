import django.newforms as forms
from django.newforms import ValidationError

import datetime

from widgets import DateTimeCombiWidget

class DateTimeCombiField(forms.MultiValueField):
    """ A newform field, which provides a seperate input tag for date and time, the output
        is merged again """
    def __init__(self, required=True, label=None, widget=None,initial=None):
        fields = (forms.DateField(),forms.TimeField())
        widget = widget or DateTimeCombiWidget()
        super(DateTimeCombiField, self).__init__(fields, required,widget, label, initial)


    def compress(self, data_list):
        if data_list:
            try:
                return datetime.datetime.combine(data_list[0], data_list[1])
            except:
                return None
        return None



