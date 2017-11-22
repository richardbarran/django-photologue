# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0003_auto_20140822_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='photos',
            field=sortedm2m.fields.SortedManyToManyField(to='photologue.Photo', related_name='galleries', null=True, verbose_name='photos', blank=True, help_text=None),
        ),
        migrations.AlterField(
            model_name='photo',
            name='effect',
            field=models.ForeignKey(to='photologue.PhotoEffect', blank=True, related_name='photo_related', verbose_name='effect', null=True),
        ),
        migrations.AlterField(
            model_name='photosize',
            name='effect',
            field=models.ForeignKey(to='photologue.PhotoEffect', blank=True, related_name='photo_sizes', verbose_name='photo effect', null=True),
        ),
        migrations.AlterField(
            model_name='photosize',
            name='watermark',
            field=models.ForeignKey(to='photologue.Watermark', blank=True, related_name='photo_sizes', verbose_name='watermark image', null=True),
        ),
    ]
