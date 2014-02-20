from django.conf.urls import patterns, include, url


from .icalendar import urls as ical_urls

urlpatterns = patterns(
    '',
    
    url(
        r'^',
        include(ical_urls),
    ),

)
