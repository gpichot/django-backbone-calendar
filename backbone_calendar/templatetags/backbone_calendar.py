from django import template
from django.utils.timezone import now

from ..models import Event


register = template.Library()


@register.inclusion_tag('backbone_calendar/events_next.html')
def display_next_events(nb=5):
    return {
        'events': Event.objects.filter(
            end__gt=now()
        ).order_by('start').select_related('agenda', 'agenda__calendar'),
    }

