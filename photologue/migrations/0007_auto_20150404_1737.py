# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0006_auto_20141028_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='photos',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='galleries', verbose_name='photos', to='photologue.Photo', blank=True),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', verbose_name='sites', blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', verbose_name='sites', blank=True),
        ),
    ]
