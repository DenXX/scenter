# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fence'
        db.create_table(u'api_fence', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=128, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('due', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('_location', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
        ))
        db.send_create_signal(u'api', ['Fence'])

        # Adding model 'ScenterUser'
        db.create_table(u'api_scenteruser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('userpic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['ScenterUser'])

        # Adding M2M table for field groups on 'ScenterUser'
        m2m_table_name = db.shorten_name(u'api_scenteruser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('scenteruser', models.ForeignKey(orm[u'api.scenteruser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['scenteruser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'ScenterUser'
        m2m_table_name = db.shorten_name(u'api_scenteruser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('scenteruser', models.ForeignKey(orm[u'api.scenteruser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['scenteruser_id', 'permission_id'])

        # Adding M2M table for field wormholes on 'ScenterUser'
        m2m_table_name = db.shorten_name(u'api_scenteruser_wormholes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('scenteruser', models.ForeignKey(orm[u'api.scenteruser'], null=False)),
            ('fence', models.ForeignKey(orm[u'api.fence'], null=False))
        ))
        db.create_unique(m2m_table_name, ['scenteruser_id', 'fence_id'])

        # Adding model 'Scent'
        db.create_table(u'api_scent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scents', to=orm['api.ScenterUser'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('due', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('fence', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scents', to=orm['api.Fence'])),
        ))
        db.send_create_signal(u'api', ['Scent'])


    def backwards(self, orm):
        # Deleting model 'Fence'
        db.delete_table(u'api_fence')

        # Deleting model 'ScenterUser'
        db.delete_table(u'api_scenteruser')

        # Removing M2M table for field groups on 'ScenterUser'
        db.delete_table(db.shorten_name(u'api_scenteruser_groups'))

        # Removing M2M table for field user_permissions on 'ScenterUser'
        db.delete_table(db.shorten_name(u'api_scenteruser_user_permissions'))

        # Removing M2M table for field wormholes on 'ScenterUser'
        db.delete_table(db.shorten_name(u'api_scenteruser_wormholes'))

        # Deleting model 'Scent'
        db.delete_table(u'api_scent')


    models = {
        u'api.fence': {
            'Meta': {'object_name': 'Fence'},
            '_location': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'api.scent': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Scent'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scents'", 'to': u"orm['api.ScenterUser']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'fence': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scents'", 'to': u"orm['api.Fence']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'api.scenteruser': {
            'Meta': {'ordering': "('username',)", 'object_name': 'ScenterUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'userpic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'wormholes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'wormhole_users'", 'symmetrical': 'False', 'to': u"orm['api.Fence']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']