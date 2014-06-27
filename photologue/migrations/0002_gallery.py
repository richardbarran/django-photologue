# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import photologue.models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '__first__'),
        ('photologue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('title', models.CharField(unique=True, max_length=50, verbose_name='title')),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', unique=True, verbose_name='title slug')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('is_public', models.BooleanField(default=True, help_text='Public galleries will be displayed in the default views.', verbose_name='is public')),
                ('tags', photologue.models.TagField(help_text='Django-tagging was not found, tags will be treated as plain text.', max_length=255, verbose_name='tags', blank=True)),
                ('photos', sortedm2m.fields.SortedManyToManyField(to='photologue.Photo', null=True, verbose_name='photos', blank=True)),
                ('sites', models.ManyToManyField(to='sites.Site', null=True, verbose_name='sites', blank=True)),
            ],
            options={
                'ordering': [b'-date_added'],
                'get_latest_by': b'date_added',
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
            },
            bases=(models.Model,),
        ),
    ]
