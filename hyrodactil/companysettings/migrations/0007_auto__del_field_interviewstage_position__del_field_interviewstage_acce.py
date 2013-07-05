# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'InterviewStage', fields ['position', 'company']
        db.delete_unique(u'companysettings_interviewstage', ['position', 'company_id'])

        # Deleting field 'InterviewStage.position'
        db.delete_column(u'companysettings_interviewstage', 'position')

        # Deleting field 'InterviewStage.accepted'
        db.delete_column(u'companysettings_interviewstage', 'accepted')

        # Deleting field 'InterviewStage.rejected'
        db.delete_column(u'companysettings_interviewstage', 'rejected')

        # Adding field 'InterviewStage.tag'
        db.add_column(u'companysettings_interviewstage', 'tag',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True),
                      keep_default=False)


        # Changing field 'InterviewStage.company'
        db.alter_column(u'companysettings_interviewstage', 'company_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'], null=True))

    def backwards(self, orm):
        # Adding field 'InterviewStage.position'
        db.add_column(u'companysettings_interviewstage', 'position',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'InterviewStage.accepted'
        db.add_column(u'companysettings_interviewstage', 'accepted',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'InterviewStage.rejected'
        db.add_column(u'companysettings_interviewstage', 'rejected',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'InterviewStage.tag'
        db.delete_column(u'companysettings_interviewstage', 'tag')


        # User chose to not deal with backwards NULL issues for 'InterviewStage.company'
        raise RuntimeError("Cannot reverse this migration. 'InterviewStage.company' and its values cannot be restored.")
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
            'Meta': {'object_name': 'InterviewStage'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']", 'null': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['companysettings']