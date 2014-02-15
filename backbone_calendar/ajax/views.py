from datetime import datetime


from django.views import generic
from django.db.models import Q


from .mixins import JSONResponseMixin
from ..models import Event


def get_start_and_end(request):
    start = datetime.fromtimestamp(int(request.POST.get('start')) / 1000)
    end = datetime.fromtimestamp(int(request.POST.get('end')) / 1000)

    return (start, end)


def event_list_as_fullcalendar(events):
    return [{
        'id': event.pk,
        'title': event.name + ' - ' + event.flat_places(),
        'start': event.start.isoformat(),
        'end': event.end.isoformat(),
        'url': event.url,
        'allDay': event.all_day,
    } for event in events]


class PlaceEventsAjaxView(JSONResponseMixin, generic.ListView):
    model = Event

    def dispatch(self, *args, **kwargs):
        return super(JSONResponseMixin, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        (start, end) = get_start_and_end(self.request)

        filter = Q(start__gt=start) & Q(end__lt=end)
        filter &= Q(places__slug=self.kwargs['place_slug'])

        events = self.model.objects.filter(
            filter,
        )

        return event_list_as_fullcalendar(events)
