from django import forms


from ..models import Event
from .fields import DateTimeAwareField


class EventForm(forms.ModelForm):
    start = DateTimeAwareField()
    end = DateTimeAwareField()

    class Meta:
        model = Event
        exclude = ()
