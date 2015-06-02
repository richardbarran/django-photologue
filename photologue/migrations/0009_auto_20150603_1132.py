# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('photologue', '0008_auto_20150509_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='canonical_site',
            field=models.ForeignKey(related_name='photologue_gallery_canonical_related', verbose_name='canonical site', blank=True, to='sites.Site', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='canonical_site',
            field=models.ForeignKey(related_name='photologue_photo_canonical_related', verbose_name='canonical site', blank=True, to='sites.Site', null=True),
            preserve_default=True,
        ),
    ]
