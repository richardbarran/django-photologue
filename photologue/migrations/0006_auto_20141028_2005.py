# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0005_auto_20141027_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galleryupload',
            name='gallery',
        ),
        migrations.DeleteModel(
            name='GalleryUpload',
        ),
    ]
