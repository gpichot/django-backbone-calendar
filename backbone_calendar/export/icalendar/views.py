from django_ical.views import ICalFeed

from ...models import Event


class EventFeed(ICalFeed):
    """
    ICalendar Exporter
    """
    
    def items(self):
        return Event.objects.all().order_by('-start')

    def item_guid(self, item):
        return "%(pk)d@" % {
            'pk': item.pk,
        }

    def item_link(self, item):
        return item.url

    def item_title(self, item):
        return item.title

    def item_start_datetime(self, item):
        return item.start

    def item_end_datetime(self, item):
        return item.end
