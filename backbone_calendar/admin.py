from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count


from .models import Calendar, Agenda, Event, Place


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    list_display = ('title', 'start', 'end', 'agenda', )
    list_filter = ('agenda__calendar', 'agenda', 'places', )


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_agendas', )
    prepopulated_fields = {
        'slug': ('name', ),
    }

    def count_agendas(self, obj):
        return obj.count_agendas
    count_agendas.short_description = _('Agendas\' count')

    def queryset(self, request):
        queryset = super(CalendarAdmin, self).queryset(request)
        return queryset.annotate(count_agendas=Count('agendas'))


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('name', 'calendar', 'count_events', )
    prepopulated_fields = {
        'slug': ('name', ),
    }

    def count_events(self, obj):
        return obj.count_events
    count_events.short_description = _('Events\' count')

    def queryset(self, request):
        queryset = super(AgendaAdmin, self).queryset(request)
        return queryset.annotate(count_events=Count('events'))


class PlaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', ),
    }


admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Place, PlaceAdmin)
