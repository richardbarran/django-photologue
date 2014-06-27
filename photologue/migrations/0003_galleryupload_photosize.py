# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0002_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zip_file', models.FileField(help_text='Select a .zip file of images to upload into a new Gallery.', upload_to=b'photologue/temp', verbose_name='images file (.zip)')),
                ('title', models.CharField(help_text='All uploaded photos will be given a title made up of this title + a sequential number.', max_length=50, verbose_name='title')),
                ('gallery', models.ForeignKey(to_field='id', blank=True, to='photologue.Gallery', help_text='Select a gallery to add these images to. Leave this empty to create a new gallery from the supplied title.', null=True, verbose_name='gallery')),
                ('caption', models.TextField(help_text='Caption will be added to all photos.', verbose_name='caption', blank=True)),
                ('description', models.TextField(help_text='A description of this Gallery.', verbose_name='description', blank=True)),
                ('is_public', models.BooleanField(default=True, help_text='Uncheck this to make the uploaded gallery and included photographs private.', verbose_name='is public')),
                ('tags', models.CharField(help_text='Django-tagging was not found, tags will be treated as plain text.', max_length=255, verbose_name='tags', blank=True)),
            ],
            options={
                'verbose_name': 'gallery upload',
                'verbose_name_plural': 'gallery uploads',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Photo size name should contain only letters, numbers and underscores. Examples: "thumbnail", "display", "small", "main_page_widget".', unique=True, max_length=40, verbose_name='name', validators=[django.core.validators.RegexValidator(regex=b'^[a-z0-9_]+$', message=b'Use only plain lowercase letters (ASCII), numbers and underscores.')])),
                ('width', models.PositiveIntegerField(default=0, help_text='If width is set to "0" the image will be scaled to the supplied height.', verbose_name='width')),
                ('height', models.PositiveIntegerField(default=0, help_text='If height is set to "0" the image will be scaled to the supplied width', verbose_name='height')),
                ('quality', models.PositiveIntegerField(default=70, help_text='JPEG image quality.', verbose_name='quality', choices=[(30, 'Very Low'), (40, 'Low'), (50, 'Medium-Low'), (60, 'Medium'), (70, 'Medium-High'), (80, 'High'), (90, 'Very High')])),
                ('upscale', models.BooleanField(default=False, help_text='If selected the image will be scaled up if necessary to fit the supplied dimensions. Cropped sizes will be upscaled regardless of this setting.', verbose_name='upscale images?')),
                ('crop', models.BooleanField(default=False, help_text='If selected the image will be scaled and cropped to fit the supplied dimensions.', verbose_name='crop to fit?')),
                ('pre_cache', models.BooleanField(default=False, help_text='If selected this photo size will be pre-cached as photos are added.', verbose_name='pre-cache?')),
                ('increment_count', models.BooleanField(default=False, help_text='If selected the image\'s "view_count" will be incremented when this photo size is displayed.', verbose_name='increment view count?')),
                ('effect', models.ForeignKey(verbose_name='photo effect', to_field='id', blank=True, to='photologue.PhotoEffect', null=True)),
                ('watermark', models.ForeignKey(verbose_name='watermark image', to_field='id', blank=True, to='photologue.Watermark', null=True)),
            ],
            options={
                'ordering': [b'width', b'height'],
                'verbose_name': 'photo size',
                'verbose_name_plural': 'photo sizes',
            },
            bases=(models.Model,),
        ),
    ]
