# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0004_auto_20140915_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(unique=True, max_length=60, verbose_name='title'),
            preserve_default=True,
        ),
    ]
