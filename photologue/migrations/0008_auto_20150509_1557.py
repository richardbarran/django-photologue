# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0007_auto_20150404_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='tags',
        ),
    ]
