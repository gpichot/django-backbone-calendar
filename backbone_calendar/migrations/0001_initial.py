# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table(u'backbone_calendar_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('planning', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'backbone_calendar', ['Place'])

        # Adding model 'Calendar'
        db.create_table(u'backbone_calendar_calendar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=30)),
        ))
        db.send_create_signal(u'backbone_calendar', ['Calendar'])

        # Adding model 'Agenda'
        db.create_table(u'backbone_calendar_agenda', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agendas', to=orm['backbone_calendar.Calendar'])),
        ))
        db.send_create_signal(u'backbone_calendar', ['Agenda'])

        # Adding model 'Event'
        db.create_table(u'backbone_calendar_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('agenda', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['backbone_calendar.Agenda'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('allDay', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'backbone_calendar', ['Event'])

        # Adding M2M table for field places on 'Event'
        m2m_table_name = db.shorten_name(u'backbone_calendar_event_places')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'backbone_calendar.event'], null=False)),
            ('place', models.ForeignKey(orm[u'backbone_calendar.place'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'place_id'])


    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table(u'backbone_calendar_place')

        # Deleting model 'Calendar'
        db.delete_table(u'backbone_calendar_calendar')

        # Deleting model 'Agenda'
        db.delete_table(u'backbone_calendar_agenda')

        # Deleting model 'Event'
        db.delete_table(u'backbone_calendar_event')

        # Removing M2M table for field places on 'Event'
        db.delete_table(db.shorten_name(u'backbone_calendar_event_places'))


    models = {
        u'backbone_calendar.agenda': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Agenda'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agendas'", 'to': u"orm['backbone_calendar.Calendar']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'backbone_calendar.calendar': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Calendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'backbone_calendar.event': {
            'Meta': {'ordering': "('start',)", 'object_name': 'Event'},
            'agenda': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': u"orm['backbone_calendar.Agenda']"}),
            'allDay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'events'", 'blank': 'True', 'to': u"orm['backbone_calendar.Place']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'backbone_calendar.place': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Place'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'planning': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['backbone_calendar']