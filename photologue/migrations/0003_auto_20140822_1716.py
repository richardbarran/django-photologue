# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0002_photosize_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryupload',
            name='title',
            field=models.CharField(null=True, help_text='All uploaded photos will be given a title made up of this title + a sequential number.', max_length=50, verbose_name='title', blank=True),
        ),
    ]
