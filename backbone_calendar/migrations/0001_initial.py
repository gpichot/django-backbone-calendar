# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=40, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'agenda',
                'verbose_name_plural': 'agendas',
            },
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=30, verbose_name='Slug')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'calendar',
                'verbose_name_plural': 'calendars',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('start', models.DateTimeField(null=True, verbose_name='Start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='End', blank=True)),
                ('url', models.URLField(null=True, verbose_name='URL', blank=True)),
                ('allDay', models.BooleanField(default=False, help_text=b'Check it if the event is an all-day event', verbose_name='All day')),
                ('agenda', models.ForeignKey(related_name='events', verbose_name='Agenda', to='backbone_calendar.Agenda')),
            ],
            options={
                'ordering': ('start',),
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('planning', models.BooleanField(default=True, help_text=b'\n            If selected forbids that two events occur at the same time\n        ', verbose_name='Planning enabled')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'place',
                'verbose_name_plural': 'places',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='places',
            field=models.ManyToManyField(related_name='events', verbose_name='Places', to='backbone_calendar.Place', blank=True),
        ),
        migrations.AddField(
            model_name='agenda',
            name='calendar',
            field=models.ForeignKey(related_name='agendas', to='backbone_calendar.Calendar'),
        ),
    ]
