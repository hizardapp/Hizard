# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Opening'
        db.create_table(u'openings_opening', (
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
        db.send_create_signal(u'openings', ['Opening'])

        # Adding M2M table for field questions on 'Opening'
        db.create_table(u'openings_opening_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('opening', models.ForeignKey(orm[u'openings.opening'], null=False)),
            ('question', models.ForeignKey(orm[u'companysettings.question'], null=False))
        ))
        db.create_unique(u'openings_opening_questions', ['opening_id', 'question_id'])


    def backwards(self, orm):
        # Deleting model 'Opening'
        db.delete_table(u'openings_opening')

        # Removing M2M table for field questions on 'Opening'
        db.delete_table('openings_opening_questions')


    models = {
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subdomain': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'companysettings.department': {
            'Meta': {'object_name': 'Department'},
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
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'textbox'", 'max_length': '20'})
        },
        u'openings.opening': {
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

    complete_apps = ['openings']