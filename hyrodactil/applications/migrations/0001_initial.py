# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Applicant'
        db.create_table(u'applications_applicant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=770)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=770)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'applications', ['Applicant'])

        # Adding model 'Application'
        db.create_table(u'applications_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.Applicant'])),
            ('opening', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openings.Opening'])),
            ('current_stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companysettings.InterviewStage'], null=True)),
        ))
        db.send_create_signal(u'applications', ['Application'])

        # Adding model 'ApplicationAnswer'
        db.create_table(u'applications_applicationanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['applications.Application'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openings.OpeningQuestion'])),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'applications', ['ApplicationAnswer'])

        # Adding model 'ApplicationStageTransition'
        db.create_table(u'applications_applicationstagetransition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stage_transitions', to=orm['applications.Application'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.CustomUser'], null=True)),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companysettings.InterviewStage'])),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'applications', ['ApplicationStageTransition'])

        # Adding model 'ApplicationMessage'
        db.create_table(u'applications_applicationmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.Application'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.CustomUser'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.ApplicationMessage'], null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'applications', ['ApplicationMessage'])

        # Adding model 'ApplicationRating'
        db.create_table(u'applications_applicationrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.Application'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.CustomUser'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'applications', ['ApplicationRating'])


    def backwards(self, orm):
        # Deleting model 'Applicant'
        db.delete_table(u'applications_applicant')

        # Deleting model 'Application'
        db.delete_table(u'applications_application')

        # Deleting model 'ApplicationAnswer'
        db.delete_table(u'applications_applicationanswer')

        # Deleting model 'ApplicationStageTransition'
        db.delete_table(u'applications_applicationstagetransition')

        # Deleting model 'ApplicationMessage'
        db.delete_table(u'applications_applicationmessage')

        # Deleting model 'ApplicationRating'
        db.delete_table(u'applications_applicationrating')


    models = {
        u'accounts.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'employees'", 'null': 'True', 'to': u"orm['companies.Company']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_company_admin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'applications.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '770'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '770'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'applications.application': {
            'Meta': {'object_name': 'Application'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.Applicant']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'current_stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companysettings.InterviewStage']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'opening': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openings.Opening']"})
        },
        u'applications.applicationanswer': {
            'Meta': {'object_name': 'ApplicationAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['applications.Application']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openings.OpeningQuestion']"})
        },
        u'applications.applicationmessage': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ApplicationMessage'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.Application']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.ApplicationMessage']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.CustomUser']"})
        },
        u'applications.applicationrating': {
            'Meta': {'object_name': 'ApplicationRating'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.Application']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.CustomUser']"})
        },
        u'applications.applicationstagetransition': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ApplicationStageTransition'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stage_transitions'", 'to': u"orm['applications.Application']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companysettings.InterviewStage']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.CustomUser']", 'null': 'True'})
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
            'Meta': {'ordering': "['position']", 'unique_together': "(('company', 'position'),)", 'object_name': 'InterviewStage'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']", 'null': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'openings.opening': {
            'Meta': {'object_name': 'Opening'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'employment_type': ('django.db.models.fields.CharField', [], {'default': "'full_time'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '770'})
        },
        u'openings.openingquestion': {
            'Meta': {'ordering': "['created']", 'object_name': 'OpeningQuestion'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'opening': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['openings.Opening']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '770'})
        }
    }

    complete_apps = ['applications']