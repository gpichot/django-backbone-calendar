from django.conf.urls import patterns, include, url

from .views import EventFeed


urlpatterns = patterns(
    '',

    url(
        r'^planning/(?P<place_slug>[\w-]+).ics$',
        EventFeed(),
        name="planning-ical",
    ),

    url(
        r'^(?P<calendar_slug>[\w-]+).ics$',
        EventFeed(),
        name="calendar-ical",
    ),

)
