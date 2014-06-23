import json

from django import template
from django.utils.timezone import now
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader, Context

from ..models import Event, Calendar


register = template.Library()


@register.inclusion_tag('backbone_calendar/events_next.html')
def display_next_events(nb=5):
    return {
        'events': Event.objects.filter(
            end__gt=now()
        ).order_by('start').select_related('agenda', 'agenda__calendar'),
    }


@register.assignment_tag(takes_context=True)
def get_calendar_display(context, *args, **kwargs):
    return CalendarDisplay(context, *args, **kwargs)


class CalendarDisplay(object):
    def __init__(self, context, id='calendar', places=None,
                 calendar=None,
                 agendas=None, editable=False):
        self.id = id

        if places is not None:
            places = places if len(places) > 0 else [places]
        if agendas is not None:
            agendas = agendas if len(agendas) > 0 else [agendas]

        self.places = places
        self.calendar = calendar
        self.agendas = agendas
        self.editable = editable
        self.context = context

    def to_json(self):
        calendar = {
            'csrf_token': unicode(self.context['csrf_token']),
            'url_root': reverse('backbone:backbone_calendar_event'),
        }     
        if self.calendar is not None and isinstance(self.calendar, Calendar):
            calendar['calendar'] = self.calendar.pk
        if self.agendas is not None:
            calendar['agendas'] = self.agendas.values_list('pk')
        if self.places is not None:
            calendar['places'] = self.places.values_list('pk')

        return mark_safe(json.dumps(calendar, cls=DjangoJSONEncoder))

    def print_list_agendas(self):
        template = loader.get_template('backbone_calendar/list_agendas.html')
        agendas = []
        if self.calendar is not None:
            agendas = self.calendar.agendas.all()
        elif self.agendas is not None:
            agendas = self.agendas
        elif self.places is not None:
            agendas = self.places.events.agendas.all()
        return template.render(Context({   
            'agendas': agendas,
        }))
    
    

@register.inclusion_tag(
    'backbone_calendar/javascripts.html',
    takes_context=True,
)
def print_javascript_scripts(context, editable=False):
    return {
        'editable': editable,
        'language_code': context['LANGUAGE_CODE'].lower(),
    }


@register.inclusion_tag('backbone_calendar/stylesheets.html')
def print_stylesheet_links():
    return {}
