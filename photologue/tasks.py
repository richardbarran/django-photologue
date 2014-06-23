from __future__ import absolute_import

from celery import shared_task
from photologue.models import Photo

@shared_task(name='photologue.tasks.pre_cache', max_retries=5)
def pre_cache(photo_id):
    # need to use concrete (not abstract) model
    image = Photo.objects.get(id=photo_id)
    image.pre_cache()
