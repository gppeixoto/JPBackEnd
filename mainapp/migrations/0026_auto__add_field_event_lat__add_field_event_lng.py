# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.lat'
        db.add_column(u'mainapp_event', 'lat',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=7),
                      keep_default=False)

        # Adding field 'Event.lng'
        db.add_column(u'mainapp_event', 'lng',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=7),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.lat'
        db.delete_column(u'mainapp_event', 'lat')

        # Deleting field 'Event.lng'
        db.delete_column(u'mainapp_event', 'lng')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mainapp.comment': {
            'Meta': {'object_name': 'Comment'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 14, 0, 0)'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Profile']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(13, 39, 30, 962762)'})
        },
        u'mainapp.event': {
            'Meta': {'object_name': 'Event'},
            'creatorProfile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creatorProfile'", 'null': 'True', 'to': u"orm['mainapp.Profile']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'localization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Localization']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mainapp.Profile']", 'symmetrical': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'private': ('django.db.models.fields.BooleanField', [], {}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Sport']"}),
            'timeBegin': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'timeEnd': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'visible': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'visible'", 'null': 'True', 'to': u"orm['mainapp.Profile']"})
        },
        u'mainapp.localization': {
            'Meta': {'object_name': 'Localization'},
            'adress': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'neighbourhood': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'mainapp.profile': {
            'Meta': {'object_name': 'Profile'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'new_token_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'mainapp.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numberOfVoters': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Profile']"}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '2.5'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Sport']"})
        },
        u'mainapp.search': {
            'Meta': {'object_name': 'Search'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Localization']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Profile']"}),
            'sport': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mainapp.Sport']", 'symmetrical': 'False'}),
            'timeBegin': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'timeEnd': ('django.db.models.fields.TimeField', [], {'null': 'True'})
        },
        u'mainapp.sport': {
            'Meta': {'object_name': 'Sport'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ratings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mainapp.Profile']", 'through': u"orm['mainapp.Rating']", 'symmetrical': 'False'})
        },
        u'mainapp.tag': {
            'Meta': {'object_name': 'Tag'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'numberOfVoters': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Profile']"})
        }
    }

    complete_apps = ['mainapp']