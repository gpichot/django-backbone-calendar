from django.views import generic


from .models import Place
from .forms import EventForm
from .mixins import CalendarEditMixin


class PlaceCalendarView(generic.DetailView):
    model = Place
    slug_url_kwarg = 'place_slug'
    context_object_name = 'place'


class PlaceCalendarEditView(CalendarEditMixin, PlaceCalendarView):

    def get_context_data(self, **kwargs):
        context = super(PlaceCalendarView, self).get_context_data(**kwargs)
        
        context_edit = CalendarEditMixin.get_context_data(self, **kwargs)

        
        context_edit['calendar_event_form'] = EventForm()

        return context_edit
