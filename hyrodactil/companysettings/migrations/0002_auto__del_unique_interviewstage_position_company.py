# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'InterviewStage', fields ['position', 'company']
        db.delete_unique(u'companysettings_interviewstage', ['position', 'company_id'])


    def backwards(self, orm):
        # Adding unique constraint on 'InterviewStage', fields ['position', 'company']
        db.create_unique(u'companysettings_interviewstage', ['position', 'company_id'])


    models = {
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subdomain': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'companysettings.interviewstage': {
            'Meta': {'ordering': "['position']", 'object_name': 'InterviewStage'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']", 'null': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['companysettings']