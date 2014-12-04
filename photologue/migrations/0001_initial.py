# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photologue.models
import django.utils.timezone
import django.core.validators
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('title', models.CharField(max_length=50, verbose_name='title', unique=True)),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', verbose_name='title slug', unique=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('is_public', models.BooleanField(help_text='Public galleries will be displayed in the default views.', verbose_name='is public', default=True)),
                ('tags', photologue.models.TagField(max_length=255, help_text='Django-tagging was not found, tags will be treated as plain text.', blank=True, verbose_name='tags')),
                ('sites', models.ManyToManyField(blank=True, verbose_name='sites', null=True, to='sites.Site')),
            ],
            options={
                'get_latest_by': 'date_added',
                'verbose_name': 'gallery',
                'ordering': ['-date_added'],
                'verbose_name_plural': 'galleries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GalleryUpload',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('zip_file', models.FileField(help_text='Select a .zip file of images to upload into a new Gallery.', verbose_name='images file (.zip)', upload_to='photologue/temp')),
                ('title', models.CharField(max_length=50, help_text='All uploaded photos will be given a title made up of this title + a sequential number.', verbose_name='title')),
                ('caption', models.TextField(help_text='Caption will be added to all photos.', blank=True, verbose_name='caption')),
                ('description', models.TextField(help_text='A description of this Gallery.', blank=True, verbose_name='description')),
                ('is_public', models.BooleanField(help_text='Uncheck this to make the uploaded gallery and included photographs private.', verbose_name='is public', default=True)),
                ('tags', models.CharField(max_length=255, help_text='Django-tagging was not found, tags will be treated as plain text.', blank=True, verbose_name='tags')),
                ('gallery', models.ForeignKey(blank=True, verbose_name='gallery', null=True, help_text='Select a gallery to add these images to. Leave this empty to create a new gallery from the supplied title.', to='photologue.Gallery')),
            ],
            options={
                'verbose_name': 'gallery upload',
                'verbose_name_plural': 'gallery uploads',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('image', models.ImageField(upload_to=photologue.models.get_storage_path, verbose_name='image')),
                ('date_taken', models.DateTimeField(verbose_name='date taken', blank=True, editable=False, null=True)),
                ('view_count', models.PositiveIntegerField(verbose_name='view count', default=0, editable=False)),
                ('crop_from', models.CharField(max_length=10, default='center', blank=True, verbose_name='crop from', choices=[('top', 'Top'), ('right', 'Right'), ('bottom', 'Bottom'), ('left', 'Left'), ('center', 'Center (Default)')])),
                ('title', models.CharField(max_length=50, verbose_name='title', unique=True)),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', verbose_name='slug', unique=True)),
                ('caption', models.TextField(blank=True, verbose_name='caption')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
                ('is_public', models.BooleanField(help_text='Public photographs will be displayed in the default views.', verbose_name='is public', default=True)),
                ('tags', photologue.models.TagField(max_length=255, help_text='Django-tagging was not found, tags will be treated as plain text.', blank=True, verbose_name='tags')),
                ('sites', models.ManyToManyField(blank=True, verbose_name='sites', null=True, to='sites.Site')),
            ],
            options={
                'get_latest_by': 'date_added',
                'verbose_name': 'photo',
                'ordering': ['-date_added'],
                'verbose_name_plural': 'photos',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gallery',
            name='photos',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, verbose_name='photos', null=True, to='photologue.Photo'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='PhotoEffect',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='name', unique=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('transpose_method', models.CharField(max_length=15, blank=True, verbose_name='rotate or flip', choices=[('FLIP_LEFT_RIGHT', 'Flip left to right'), ('FLIP_TOP_BOTTOM', 'Flip top to bottom'), ('ROTATE_90', 'Rotate 90 degrees counter-clockwise'), ('ROTATE_270', 'Rotate 90 degrees clockwise'), ('ROTATE_180', 'Rotate 180 degrees')])),
                ('color', models.FloatField(help_text='A factor of 0.0 gives a black and white image, a factor of 1.0 gives the original image.', verbose_name='color', default=1.0)),
                ('brightness', models.FloatField(help_text='A factor of 0.0 gives a black image, a factor of 1.0 gives the original image.', verbose_name='brightness', default=1.0)),
                ('contrast', models.FloatField(help_text='A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the original image.', verbose_name='contrast', default=1.0)),
                ('sharpness', models.FloatField(help_text='A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image.', verbose_name='sharpness', default=1.0)),
                ('filters', models.CharField(max_length=200, help_text='Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE". Image filters will be applied in order. The following filters are available: BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE.', blank=True, verbose_name='filters')),
                ('reflection_size', models.FloatField(help_text='The height of the reflection as a percentage of the orignal image. A factor of 0.0 adds no reflection, a factor of 1.0 adds a reflection equal to the height of the orignal image.', verbose_name='size', default=0)),
                ('reflection_strength', models.FloatField(help_text='The initial opacity of the reflection gradient.', verbose_name='strength', default=0.6)),
                ('background_color', models.CharField(max_length=7, help_text='The background color of the reflection gradient. Set this to match the background color of your page.', verbose_name='color', default='#FFFFFF')),
            ],
            options={
                'verbose_name': 'photo effect',
                'verbose_name_plural': 'photo effects',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photo',
            name='effect',
            field=models.ForeignKey(blank=True, verbose_name='effect', null=True, to='photologue.PhotoEffect'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='PhotoSize',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=40, help_text='Photo size name should contain only letters, numbers and underscores. Examples: "thumbnail", "display", "small", "main_page_widget".', verbose_name='name', unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-z0-9_]+$', message='Use only plain lowercase letters (ASCII), numbers and underscores.')])),
                ('width', models.PositiveIntegerField(help_text='If width is set to "0" the image will be scaled to the supplied height.', verbose_name='width', default=0)),
                ('height', models.PositiveIntegerField(help_text='If height is set to "0" the image will be scaled to the supplied width', verbose_name='height', default=0)),
                ('quality', models.PositiveIntegerField(help_text='JPEG image quality.', verbose_name='quality', choices=[(30, 'Very Low'), (40, 'Low'), (50, 'Medium-Low'), (60, 'Medium'), (70, 'Medium-High'), (80, 'High'), (90, 'Very High')], default=70)),
                ('upscale', models.BooleanField(help_text='If selected the image will be scaled up if necessary to fit the supplied dimensions. Cropped sizes will be upscaled regardless of this setting.', verbose_name='upscale images?', default=False)),
                ('crop', models.BooleanField(help_text='If selected the image will be scaled and cropped to fit the supplied dimensions.', verbose_name='crop to fit?', default=False)),
                ('pre_cache', models.BooleanField(help_text='If selected this photo size will be pre-cached as photos are added.', verbose_name='pre-cache?', default=False)),
                ('increment_count', models.BooleanField(help_text='If selected the image\'s "view_count" will be incremented when this photo size is displayed.', verbose_name='increment view count?', default=False)),
                ('effect', models.ForeignKey(blank=True, verbose_name='photo effect', null=True, to='photologue.PhotoEffect')),
            ],
            options={
                'verbose_name': 'photo size',
                'ordering': ['width', 'height'],
                'verbose_name_plural': 'photo sizes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Watermark',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='name', unique=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', models.ImageField(upload_to='photologue/watermarks', verbose_name='image')),
                ('style', models.CharField(max_length=5, default='scale', verbose_name='style', choices=[('tile', 'Tile'), ('scale', 'Scale')])),
                ('opacity', models.FloatField(help_text='The opacity of the overlay.', verbose_name='opacity', default=1)),
            ],
            options={
                'verbose_name': 'watermark',
                'verbose_name_plural': 'watermarks',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photosize',
            name='watermark',
            field=models.ForeignKey(blank=True, verbose_name='watermark image', null=True, to='photologue.Watermark'),
            preserve_default=True,
        ),
    ]
