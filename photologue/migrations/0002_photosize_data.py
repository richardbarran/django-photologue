# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


def initial_photosizes(apps, schema_editor):

    PhotoSize = apps.get_model('photologue', 'PhotoSize')

    # If there are already Photosizes, then we are upgrading an existing
    # installation, we don't want to auto-create some PhotoSizes.
    if PhotoSize.objects.all().count() > 0:
        return
    PhotoSize.objects.create(name='admin_thumbnail',
                             width=100,
                             height=75,
                             crop=True,
                             pre_cache=True,
                             increment_count=False)
    PhotoSize.objects.create(name='thumbnail',
                             width=100,
                             height=75,
                             crop=True,
                             pre_cache=True,
                             increment_count=False)
    PhotoSize.objects.create(name='display',
                             width=400,
                             crop=False,
                             pre_cache=True,
                             increment_count=True)


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_photosizes),
    ]
