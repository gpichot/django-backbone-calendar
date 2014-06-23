from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class Place(models.Model):
    """
        Define a place where an event can be set.
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=100,
        unique=True,
    )
    planning = models.BooleanField(
        _('Planning enabled'),
        default=True,
        help_text="""
            If selected forbids that two events occur at the same time
        """
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = _('place')
        verbose_name_plural = _('places')


class Calendar(models.Model):
    """
        A calendar is used to store multiple agendas.
    """
    name = models.CharField(
        _('Name'),
        max_length=30,
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=30,
        unique=True,
    )

    def __unicode__(self):
        return self.name

    def agenda_pks(self):
        return self.agendas.values_list('pk', flat=True)

    def get_absolute_url(self):
        return reverse("calendar-detail", kwargs={
            'calendar_slug': self.slug,
        })

    def get_icalendar_url(self):
        return reverse("calendar-ical", kwargs={
            'calendar_slug': self.slug,
        })

    class Meta:
        ordering = ('name', )
        verbose_name = _('calendar')
        verbose_name_plural = _('calendars')


class Agenda(models.Model):
    """
        An agenda is used to store the items which belong to the same
        category.
    """
    name = models.CharField(
        _('Name'),
        max_length=40,
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=40,
        unique=True,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
    )
    calendar = models.ForeignKey(
        Calendar,
        related_name="agendas",
    )

    def __unicode__(self):
        return '%(calendar)s - %(agenda)s' % {
            'calendar': self.calendar,
            'agenda': self.name,
        }

    class Meta:
        ordering = ('name', )
        verbose_name = _('agenda')
        verbose_name_plural = _('agendas')


class Event(models.Model):
    """
        This model represent an event.
    """
    title = models.CharField(
        _('Title'),
        max_length=60,
    )
    start = models.DateTimeField(
        _('Start'),
        blank=True,
        null=True,
    )
    end = models.DateTimeField(
        _('End'),
        blank=True,
        null=True,
    )
    agenda = models.ForeignKey(
        Agenda,
        related_name="events",
        verbose_name=_('Agenda'),
    )
    places = models.ManyToManyField(
        Place,
        related_name="events",
        verbose_name=_('Places'),
        blank=True,
    )
    url = models.URLField(
        _('URL'),
        blank=True,
        null=True,
    )
    allDay = models.BooleanField(
        _('All day'),
        default=False,
        help_text="Check it if the event is an all-day event",
    )

    def flat_places(self):
        return ', '.join([unicode(x) for x in self.places.all()])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('start', )
        verbose_name = _('event')
        verbose_name_plural = _('events')
