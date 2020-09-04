import os
from io import BytesIO
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from PIL import Image
from django.contrib.sites.models import Site
import zipfile
from photologue.models import Photo, Gallery
import logging
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

logger = logging.getLogger('photologue.zip')


def handle_zip(zip_upload_model, request=None):
    _parse_zip(zip_upload_model.zip_file, zip_upload_model.gallery, zip_upload_model.title, zip_upload_model.description,
               zip_upload_model.caption,
               zip_upload_model.is_public, request=request)


def _parse_zip(zip_file, gallery, title, description, caption, is_public, request=None):
    zip = zipfile.ZipFile(zip_file)
    count = 1
    current_site = Site.objects.get(id=settings.SITE_ID)
    if gallery:
        logger.debug('Using pre-existing gallery.')
    else:
        logger.debug(
            force_text('Creating new gallery "{0}".').format(title))
        gallery = Gallery.objects.create(title=title,
                                         slug=slugify(title),
                                         description=description,
                                         is_public=is_public)
        gallery.sites.add(current_site)

    for filename in sorted(zip.namelist()):

        logger.debug('Reading file "{}".'.format(filename))

        if filename.startswith('__') or filename.startswith('.'):
            logger.debug('Ignoring file "{}".'.format(filename))
            continue

        if os.path.dirname(filename):
            logger.warning('Ignoring file "{}" as it is in a subfolder; all images should be in the top '
                           'folder of the zip.'.format(filename))
            if request:
                messages.warning(request,
                                 _('Ignoring file "{filename}" as it is in a subfolder; all images should '
                                   'be in the top folder of the zip.').format(filename=filename),
                                 fail_silently=True)
            continue

        data = zip.read(filename)

        if not len(data):
            logger.debug('File "{}" is empty.'.format(filename))
            continue

        photo_title_root = title if title else gallery.title

        # A photo might already exist with the same slug. So it's somewhat inefficient,
        # but we loop until we find a slug that's available.
        while True:
            photo_title = ' '.join([photo_title_root, str(count)])
            slug = slugify(photo_title)
            if Photo.objects.filter(slug=slug).exists():
                count += 1
                continue
            break

        photo = Photo(title=photo_title,
                      slug=slug,
                      caption=caption,
                      is_public=is_public)

        # Basic check that we have a valid image.
        try:
            file = BytesIO(data)
            opened = Image.open(file)
            opened.verify()
        except Exception:
            # Pillow doesn't recognize it as an image.
            # If a "bad" file is found we just skip it.
            # But we do flag this both in the logs and to the user.
            logger.error('Could not process file "{}" in the .zip archive.'.format(
                filename))
            if request:
                messages.warning(request,
                                 _('Could not process file "{0}" in the .zip archive.').format(
                                     filename),
                                 fail_silently=True)
            continue

        contentfile = ContentFile(data)
        photo.image.save(filename, contentfile)

        # running_in_task is ignored if not in async mode.
        # This function shouldn't care about async or not
        photo.save(running_in_task=True)

        photo.sites.add(current_site)
        gallery.photos.add(photo)
        count += 1

    zip.close()

    if request:
        messages.success(request,
                         _('The photos have been added to gallery "{0}".').format(
                             gallery.title),
                         fail_silently=True)
