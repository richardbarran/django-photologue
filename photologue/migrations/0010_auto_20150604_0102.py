# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.contrib.sites.models import Site

MULTISITE = getattr(settings, 'PHOTOLOGUE_MULTISITE', False)

def set_canonical_non_multisite(apps, schema_editor):
    Gallery = apps.get_model("photologue", "Gallery")
    Story = apps.get_model("photologue", "Gallery")
    if not MULTISITE:
        current_site = Site.objects.get_current()
        Gallery.objects.update(canonical_site=current_site)
        Story.objects.update(canonical_site=current_site)

    #Do we need to do anything for not multisite? 
    

class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0009_auto_20150603_1132'),
    ]

    operations = [
        migrations.RunPython(set_canonical_non_multisite),
    ]
