from django.conf.urls import patterns, include, url


from .views import PlaceEventsAjaxView


urlpatterns = patterns('',

    # Event list for a place
    url(
        r'(?P<place_slug>[\w-]+)/events.json',
        PlaceEventsAjaxView.as_view(),
        name="calendar-ajax-place-events",
    ),

)
