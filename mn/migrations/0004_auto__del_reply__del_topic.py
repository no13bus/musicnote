# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Reply'
        db.delete_table(u'mn_reply')

        # Deleting model 'Topic'
        db.delete_table(u'mn_topic')


    def backwards(self, orm):
        # Adding model 'Reply'
        db.create_table(u'mn_reply', (
            ('content', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mn.Topic'])),
            ('last_touched', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 30, 0, 0), blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 30, 0, 0), blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('up_vote', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('down_vote', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 30, 0, 0), blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'mn', ['Reply'])

        # Adding model 'Topic'
        db.create_table(u'mn_topic', (
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mn.Node'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('hits', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('last_touched', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 30, 0, 0), blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='author', to=orm['auth.User'])),
            ('reply_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('up_vote', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('down_vote', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 30, 0, 0), blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 30, 0, 0), blank=True)),
            ('last_replied_time', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 30, 0, 0), blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('last_replied_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='last_replied_by', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=140)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'mn', ['Topic'])


    models = {
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mn.node': {
            'Meta': {'object_name': 'Node'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 30, 0, 0)', 'blank': 'True'}),
            'custom_style': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'limit_reputation': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'plane': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mn.Plane']"}),
            'slug': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'thumb': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'topic_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 30, 0, 0)', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        u'mn.plane': {
            'Meta': {'object_name': 'Plane'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 30, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 30, 0, 0)', 'blank': 'True'})
        },
        u'mn.userprofile': {
            'Meta': {'object_name': 'Userprofile'},
            'avatar': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'balance': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 30, 0, 0)', 'blank': 'True'}),
            'douban': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'github': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 30, 0, 0)', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'self_intro': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'signature': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'twitter': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 30, 0, 0)', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['mn']