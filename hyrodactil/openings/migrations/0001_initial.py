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
            ('department', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('employment_type', self.gf('django.db.models.fields.CharField')(default='full_time', max_length=20)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'])),
        ))
        db.send_create_signal(u'openings', ['Opening'])

        # Adding model 'OpeningQuestion'
        db.create_table(u'openings_openingquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=770)),
            ('opening', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['openings.Opening'])),
        ))
        db.send_create_signal(u'openings', ['OpeningQuestion'])


    def backwards(self, orm):
        # Deleting model 'Opening'
        db.delete_table(u'openings_opening')

        # Deleting model 'OpeningQuestion'
        db.delete_table(u'openings_openingquestion')


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

    complete_apps = ['openings']