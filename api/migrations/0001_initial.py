# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fence'
        db.create_table(u'api_fence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('due', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
        ))
        db.send_create_signal(u'api', ['Fence'])

        # Adding model 'ScentType'
        db.create_table(u'api_scenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'api', ['ScentType'])

        # Adding model 'Scent'
        db.create_table(u'api_scent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.ScentType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('due', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('fence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Fence'])),
        ))
        db.send_create_signal(u'api', ['Scent'])


    def backwards(self, orm):
        # Deleting model 'Fence'
        db.delete_table(u'api_fence')

        # Deleting model 'ScentType'
        db.delete_table(u'api_scenttype')

        # Deleting model 'Scent'
        db.delete_table(u'api_scent')


    models = {
        u'api.fence': {
            'Meta': {'object_name': 'Fence'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'api.scent': {
            'Meta': {'object_name': 'Scent'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'fence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Fence']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.ScentType']"})
        },
        u'api.scenttype': {
            'Meta': {'object_name': 'ScentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['api']