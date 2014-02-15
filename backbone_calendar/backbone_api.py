from django.forms import widgets
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _

import backbone

from .models import Event
from .forms import EventForm


class EventApiView(backbone.views.BackboneAPIView):
    model = Event
    form = EventForm
    display_fields = (
        'title', 'start', 'end', 'agenda', 
        'places', 'allDay', 'url',
    )

    def get(self, request, id=None, **kwargs):
        if not id:
            self.start = self.request.GET.get('start')
            self.end = self.request.GET.get('end')

            if not self.start or not self.end:
                return HttpResponseBadRequest(
                    _('Invalid request : `start` and `end` parameters are both required.')
                )
        return super(EventApiView, self).get(request, id, **kwargs)


    def queryset(self, request):
        qs = super(EventApiView, self).queryset(request)

        if request.method is 'GET':
            places = self.request.GET.get('places[]', [])

            filter = Q(start__gte=self.start, end__lte=self.end)
            if len(places) > 0:
                filter &= Q(places__in=places)

            qs = qs.filter(filter)

        return qs

    
backbone.site.register(EventApiView)
