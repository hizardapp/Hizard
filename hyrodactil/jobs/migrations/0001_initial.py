# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Opening'
        db.create_table(u'jobs_opening', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=770)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companysettings.Department'], null=True, blank=True)),
            ('closing_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('loc_country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
            ('loc_city', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('loc_postcode', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'])),
        ))
        db.send_create_signal(u'jobs', ['Opening'])

        # Adding M2M table for field questions on 'Opening'
        db.create_table(u'jobs_opening_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('opening', models.ForeignKey(orm[u'jobs.opening'], null=False)),
            ('question', models.ForeignKey(orm[u'companysettings.question'], null=False))
        ))
        db.create_unique(u'jobs_opening_questions', ['opening_id', 'question_id'])

        # Adding model 'Application'
        db.create_table(u'jobs_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=770)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=770)),
            ('opening', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Opening'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companysettings.InterviewStage'], null=True, blank=True)),
        ))
        db.send_create_signal(u'jobs', ['Application'])

        # Adding model 'ApplicationAnswer'
        db.create_table(u'jobs_applicationanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companysettings.Question'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Application'])),
        ))
        db.send_create_signal(u'jobs', ['ApplicationAnswer'])


    def backwards(self, orm):
        # Deleting model 'Opening'
        db.delete_table(u'jobs_opening')

        # Removing M2M table for field questions on 'Opening'
        db.delete_table('jobs_opening_questions')

        # Deleting model 'Application'
        db.delete_table(u'jobs_application')

        # Deleting model 'ApplicationAnswer'
        db.delete_table(u'jobs_applicationanswer')


    models = {
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'companysettings.department': {
            'Meta': {'object_name': 'Department'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'companysettings.interviewstage': {
            'Meta': {'object_name': 'InterviewStage'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'companysettings.question': {
            'Meta': {'object_name': 'Question'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '770', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'textbox'", 'max_length': '20'})
        },
        u'jobs.application': {
            'Meta': {'object_name': 'Application'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '770'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '770'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'opening': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Opening']"}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companysettings.InterviewStage']", 'null': 'True', 'blank': 'True'})
        },
        u'jobs.applicationanswer': {
            'Meta': {'object_name': 'ApplicationAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Application']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companysettings.Question']"})
        },
        u'jobs.opening': {
            'Meta': {'object_name': 'Opening'},
            'closing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companysettings.Department']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loc_city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'loc_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'loc_postcode': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['companysettings.Question']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '770'})
        }
    }

    complete_apps = ['jobs']