from celery import shared_task
from .models import ZipUploadModel, Photo
from .utils.zipfile import handle_zip


@shared_task(name='galleries.tasks.pre_cache', max_retries=5)
def pre_cache(photo_id):
    image = Photo.objects.get(id=photo_id)
    image.pre_cache()


@shared_task(name='galleries.tasks.parse_zip', max_retries=5)
def parse_zip(zip_file_id):
    instance = ZipUploadModel.objects.get(id=zip_file_id)
    handle_zip(instance)
    instance.zip_file.delete(False)
    instance.delete()
