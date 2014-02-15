from django.conf.urls import patterns, include, url

import backbone
backbone.autodiscover()

from .views import PlaceCalendarView, PlaceCalendarEditView


urlpatterns = patterns(
    '',

    # Backbone API
    url(
        r'^backbone/',
        include(backbone.site.urls),
    ),

    # Ajax Views
    url(
        r'ajax/',
        include('backbone_calendar.ajax.urls'),
    ),

    # Planning Edit
    url(
        r'^(?P<place_slug>[\w-]+)/planning$',
        PlaceCalendarView.as_view(),
        name="calendar-planning",
    ),
    # Planning Edit
    url(
        r'^(?P<place_slug>[\w-]+)/planning/edit$',
        PlaceCalendarEditView.as_view(),
        name="calendar-planning-edit",
    ),

)
