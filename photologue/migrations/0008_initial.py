# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gallery'
        db.create_table('photologue_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tags', self.gf('photologue.models.TagField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('photologue', ['Gallery'])


        # Adding SortedM2M table for field photos on 'Gallery'
        db.create_table('photologue_gallery_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gallery', models.ForeignKey(orm['photologue.gallery'], null=False)),
            ('photo', models.ForeignKey(orm['photologue.photo'], null=False)),
            ('sort_value', models.IntegerField())
        ))
        db.create_unique('photologue_gallery_photos', ['gallery_id', 'photo_id'])
        # Adding M2M table for field sites on 'Gallery'
        m2m_table_name = db.shorten_name('photologue_gallery_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gallery', models.ForeignKey(orm['photologue.gallery'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gallery_id', 'site_id'])

        # Adding model 'GalleryUpload'
        db.create_table('photologue_galleryupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['photologue.Gallery'], blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('photologue', ['GalleryUpload'])

        # Adding model 'Photo'
        db.create_table('photologue_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('crop_from', self.gf('django.db.models.fields.CharField')(max_length=10, default='center', blank=True)),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='photo_related', to=orm['photologue.PhotoEffect'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tags', self.gf('photologue.models.TagField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('photologue', ['Photo'])

        # Adding M2M table for field sites on 'Photo'
        m2m_table_name = db.shorten_name('photologue_photo_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm['photologue.photo'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photo_id', 'site_id'])

        # Adding model 'PhotoEffect'
        db.create_table('photologue_photoeffect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transpose_method', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('color', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('brightness', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('contrast', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('sharpness', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('filters', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('reflection_size', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('reflection_strength', self.gf('django.db.models.fields.FloatField')(default=0.6)),
            ('background_color', self.gf('django.db.models.fields.CharField')(max_length=7, default='#FFFFFF')),
        ))
        db.send_create_signal('photologue', ['PhotoEffect'])

        # Adding model 'Watermark'
        db.create_table('photologue_watermark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=5, default='scale')),
            ('opacity', self.gf('django.db.models.fields.FloatField')(default=1)),
        ))
        db.send_create_signal('photologue', ['Watermark'])

        # Adding model 'PhotoSize'
        db.create_table('photologue_photosize', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('quality', self.gf('django.db.models.fields.PositiveIntegerField')(default=70)),
            ('upscale', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('crop', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pre_cache', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('increment_count', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='photo_sizes', to=orm['photologue.PhotoEffect'], blank=True)),
            ('watermark', self.gf('django.db.models.fields.related.ForeignKey')(null=True, related_name='photo_sizes', to=orm['photologue.Watermark'], blank=True)),
        ))
        db.send_create_signal('photologue', ['PhotoSize'])


    def backwards(self, orm):
        # Deleting model 'Gallery'
        db.delete_table('photologue_gallery')

        # Removing M2M table for field photos on 'Gallery'
        db.delete_table(db.shorten_name('photologue_gallery_photos'))

        # Removing M2M table for field sites on 'Gallery'
        db.delete_table(db.shorten_name('photologue_gallery_sites'))

        # Deleting model 'GalleryUpload'
        db.delete_table('photologue_galleryupload')

        # Deleting model 'Photo'
        db.delete_table('photologue_photo')

        # Removing M2M table for field sites on 'Photo'
        db.delete_table(db.shorten_name('photologue_photo_sites'))

        # Deleting model 'PhotoEffect'
        db.delete_table('photologue_photoeffect')

        # Deleting model 'Watermark'
        db.delete_table('photologue_watermark')

        # Deleting model 'PhotoSize'
        db.delete_table('photologue_photosize')


    models = {
        'photologue.gallery': {
            'Meta': {'object_name': 'Gallery', 'ordering': "['-date_added']"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'photos': ('sortedm2m.fields.SortedManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'related_name': "'galleries'", 'to': "orm['photologue.Photo']", 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'tags': ('photologue.models.TagField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'photologue.galleryupload': {
            'Meta': {'object_name': 'GalleryUpload'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['photologue.Gallery']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zip_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'photologue.photo': {
            'Meta': {'object_name': 'Photo', 'ordering': "['-date_added']"},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'center'", 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'photo_related'", 'to': "orm['photologue.PhotoEffect']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['sites.Site']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'tags': ('photologue.models.TagField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '7', 'default': "'#FFFFFF'"}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.6'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'photologue.photosize': {
            'Meta': {'object_name': 'PhotoSize', 'ordering': "['width', 'height']"},
            'crop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'photo_sizes'", 'to': "orm['photologue.PhotoEffect']", 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'increment_count': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'pre_cache': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '70'}),
            'upscale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'watermark': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'photo_sizes'", 'to': "orm['photologue.Watermark']", 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'photologue.watermark': {
            'Meta': {'object_name': 'Watermark'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'}),
            'opacity': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '5', 'default': "'scale'"})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'", 'object_name': 'Site', 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['photologue']