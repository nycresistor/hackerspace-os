from django.forms import ModelForm
import django.forms as forms

from fields import DateTimeCombiField
from models import Event


class EventForm(ModelForm):
    startDate = DateTimeCombiField()
    endDate = DateTimeCombiField(required=False)
    teaser = forms.CharField(required=False)

    class Meta:
        model = Event
        exclude = ('where','startDate','endDate','created_at','created_by','deleted','who')



