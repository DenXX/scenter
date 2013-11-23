# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Fence.location'
        db.delete_column(u'api_fence', 'location')

        # Adding field 'Fence._location'
        db.add_column(u'api_fence', '_location',
                      self.gf('django.contrib.gis.db.models.fields.PolygonField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Fence.location'
        db.add_column(u'api_fence', 'location',
                      self.gf('django.contrib.gis.db.models.fields.PolygonField')(default=''),
                      keep_default=False)

        # Deleting field 'Fence._location'
        db.delete_column(u'api_fence', '_location')


    models = {
        u'api.fence': {
            'Meta': {'object_name': 'Fence'},
            '_location': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'api.scent': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Scent'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'fence': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scents'", 'to': u"orm['api.Fence']"}),
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