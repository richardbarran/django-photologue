# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import photologue.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoEffect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('transpose_method', models.CharField(blank=True, max_length=15, verbose_name='rotate or flip', choices=[(b'FLIP_LEFT_RIGHT', 'Flip left to right'), (b'FLIP_TOP_BOTTOM', 'Flip top to bottom'), (b'ROTATE_90', 'Rotate 90 degrees counter-clockwise'), (b'ROTATE_270', 'Rotate 90 degrees clockwise'), (b'ROTATE_180', 'Rotate 180 degrees')])),
                ('color', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a black and white image, a factor of 1.0 gives the original image.', verbose_name='color')),
                ('brightness', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a black image, a factor of 1.0 gives the original image.', verbose_name='brightness')),
                ('contrast', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the original image.', verbose_name='contrast')),
                ('sharpness', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image.', verbose_name='sharpness')),
                ('filters', models.CharField(help_text='Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE". Image filters will be applied in order. The following filters are available: BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE.', max_length=200, verbose_name='filters', blank=True)),
                ('reflection_size', models.FloatField(default=0, help_text='The height of the reflection as a percentage of the orignal image. A factor of 0.0 adds no reflection, a factor of 1.0 adds a reflection equal to the height of the orignal image.', verbose_name='size')),
                ('reflection_strength', models.FloatField(default=0.6, help_text='The initial opacity of the reflection gradient.', verbose_name='strength')),
                ('background_color', models.CharField(default=b'#FFFFFF', help_text='The background color of the reflection gradient. Set this to match the background color of your page.', max_length=7, verbose_name='color')),
            ],
            options={
                'verbose_name': 'photo effect',
                'verbose_name_plural': 'photo effects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Watermark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('image', models.ImageField(upload_to=b'photologue/watermarks', verbose_name='image')),
                ('style', models.CharField(default=b'scale', max_length=5, verbose_name='style', choices=[(b'tile', 'Tile'), (b'scale', 'Scale')])),
                ('opacity', models.FloatField(default=1, help_text='The opacity of the overlay.', verbose_name='opacity')),
            ],
            options={
                'verbose_name': 'watermark',
                'verbose_name_plural': 'watermarks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=photologue.models.get_storage_path, verbose_name='image')),
                ('date_taken', models.DateTimeField(verbose_name='date taken', null=True, editable=False, blank=True)),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count', editable=False)),
                ('crop_from', models.CharField(default=b'center', max_length=10, verbose_name='crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center (Default)')])),
                ('effect', models.ForeignKey(verbose_name='effect', to_field='id', blank=True, to='photologue.PhotoEffect', null=True)),
                ('title', models.CharField(unique=True, max_length=50, verbose_name='title')),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', unique=True, verbose_name='slug')),
                ('caption', models.TextField(verbose_name='caption', blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
                ('is_public', models.BooleanField(default=True, help_text='Public photographs will be displayed in the default views.', verbose_name='is public')),
                ('tags', photologue.models.TagField(help_text='Django-tagging was not found, tags will be treated as plain text.', max_length=255, verbose_name='tags', blank=True)),
                ('sites', models.ManyToManyField(to='sites.Site', null=True, verbose_name='sites', blank=True)),
            ],
            options={
                'ordering': [b'-date_added'],
                'get_latest_by': b'date_added',
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
            bases=(models.Model,),
        ),
    ]
