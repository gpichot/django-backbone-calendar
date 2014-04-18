from django.conf.urls import url, include

from modular_blocks import ModuleApp, TemplateTagBlock, modules

from . import urls

class BackboneCalendarModule(ModuleApp):
    app_name = 'backbone_calendar'
    name = 'backbone-calendar'
    urls = url(r'^calendar/', include(urls))
    templatetag_blocks = [
        TemplateTagBlock(
            name='calendar-events',
            library='backbone_calendar',
            tag='display_next_events',
            cache_time=60,
            kwargs={
                'nb': 5,
            }
        ),
    ]
modules.register(BackboneCalendarModule)
