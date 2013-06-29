# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Opening.department' to match new field type.
        db.rename_column(u'openings_opening', 'department_id', 'department')
        # Changing field 'Opening.department'
        db.alter_column(u'openings_opening', 'department', self.gf('django.db.models.fields.CharField')(default='', max_length=128))
        # Removing index on 'Opening', fields ['department']
        db.delete_index(u'openings_opening', ['department_id'])


    def backwards(self, orm):
        # Adding index on 'Opening', fields ['department']
        db.create_index(u'openings_opening', ['department_id'])


        # Renaming column for 'Opening.department' to match new field type.
        db.rename_column(u'openings_opening', 'department', 'department_id')
        # Changing field 'Opening.department'
        db.alter_column(u'openings_opening', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companysettings.Department'], null=True, on_delete=models.SET_NULL))

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
        u'companysettings.question': {
            'Meta': {'object_name': 'Question'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'type_field': ('django.db.models.fields.CharField', [], {'default': "'textbox'", 'max_length': '20'})
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
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['companysettings.Question']", 'null': 'True', 'through': u"orm['openings.OpeningQuestion']", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '770'})
        },
        u'openings.openingquestion': {
            'Meta': {'object_name': 'OpeningQuestion'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'opening': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openings.Opening']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companysettings.Question']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['openings']