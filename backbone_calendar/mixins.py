from .forms import EventForm


class CalendarEditMixin(object):

    def get_context_data(self, **kwargs):
        context = super(CalendarEditMixin, self).get_context_data(**kwargs)

        context['editable_calendar'] = True

        context['calendar_event_form'] = EventForm()

        return context
