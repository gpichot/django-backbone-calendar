from django.views import generic


from .models import Place, Calendar
from .mixins import CalendarEditMixin


class PlaceCalendarView(generic.DetailView):
    model = Place
    slug_url_kwarg = 'place_slug'
    context_object_name = 'place'


class PlaceCalendarEditView(CalendarEditMixin, PlaceCalendarView):
    pass


class CalendarView(generic.DetailView):
    model = Calendar
    slug_url_kwarg = 'calendar_slug'
    context_object_name = 'calendar'


class CalendarEditView(CalendarEditMixin, CalendarView):
    pass
