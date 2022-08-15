import logging
import os
import zipfile
from io import BytesIO
from typing import List
from zipfile import BadZipFile

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .models import Gallery, Photo

logger = logging.getLogger('photologue.forms')

MessageSeverity = int
MessageContent = str


class PhotoDefaults:
    title: str
    caption: str
    is_public: bool

    def __init__(self, title: str, caption: str, is_public: bool) -> "PhotoDefaults":
        self.title = title
        self.caption = caption
        self.is_public = is_public


class UploadMessage:
    severity: MessageSeverity
    content: MessageContent

    def __init__(self, severity: MessageSeverity, content: MessageContent) -> "UploadMessage":
        self.severity = severity
        self.content = content

    def success(content: MessageContent):
        return UploadMessage(severity=constants.SUCCESS, content=content)

    def warning(content: MessageContent):
        return UploadMessage(severity=constants.WARNING, content=content)


class UploadZipForm(forms.Form):
    zip_file = forms.FileField()

    title = forms.CharField(label=_('Title'),
                            max_length=250,
                            required=False,
                            help_text=_('All uploaded photos will be given a title made up of this title + a '
                                        'sequential number.<br>This field is required if creating a new '
                                        'gallery, but is optional when adding to an existing gallery - if '
                                        'not supplied, the photo titles will be creating from the existing '
                                        'gallery name.'))
    gallery = forms.ModelChoiceField(Gallery.objects.all(),
                                     label=_('Gallery'),
                                     required=False,
                                     help_text=_('Select a gallery to add these images to. Leave this empty to '
                                                 'create a new gallery from the supplied title.'))
    caption = forms.CharField(label=_('Caption'),
                              required=False,
                              help_text=_('Caption will be added to all photos.'))
    description = forms.CharField(label=_('Description'),
                                  required=False,
                                  help_text=_('A description of this Gallery. Only required for new galleries.'))
    is_public = forms.BooleanField(label=_('Is public'),
                                   initial=True,
                                   required=False,
                                   help_text=_('Uncheck this to make the uploaded '
                                               'gallery and included photographs private.'))

    def clean_zip_file(self):
        """Open the zip file a first time, to check that it is a valid zip archive.
        We'll open it again in a moment, so we have some duplication, but let's focus
        on keeping the code easier to read!
        """
        zip_file = self.cleaned_data['zip_file']
        try:
            zip = zipfile.ZipFile(zip_file)
        except BadZipFile as e:
            raise forms.ValidationError(str(e))
        bad_file = zip.testzip()
        if bad_file:
            zip.close()
            raise forms.ValidationError('"%s" in the .zip archive is corrupt.' % bad_file)
        zip.close()  # Close file in all cases.
        return zip_file

    def clean_title(self):
        title = self.cleaned_data['title']
        if title and Gallery.objects.filter(title=title).exists():
            raise forms.ValidationError(_('A gallery with that title already exists.'))
        return title

    def clean(self):
        cleaned_data = super().clean()
        if not self['title'].errors:
            # If there's already an error in the title, no need to add another
            # error related to the same field.
            if not cleaned_data.get('title', None) and not cleaned_data['gallery']:
                raise forms.ValidationError(
                    _('Select an existing gallery, or enter a title for a new gallery.'))
        return cleaned_data

    def save(self, request=None, zip_file=None):
        if not zip_file:
            zip_file = self.cleaned_data['zip_file']

        zip = zipfile.ZipFile(zip_file)
        photo_defaults = PhotoDefaults(
            title=self.cleaned_data["title"], caption=self.cleaned_data["caption"],
            is_public=self.cleaned_data["is_public"])
        current_site = Site.objects.get(id=settings.SITE_ID)

        gallery = self._reuse_or_create_gallery_in_site(current_site)

        upload_messages = upload_photos_to_site(current_site, zip, gallery, photo_defaults)

        if request:
            for upload_message in upload_messages:
                messages.add_message(request, upload_message.severity, upload_message.content, fail_silently=True)

    def _reuse_or_create_gallery_in_site(self, current_site):
        if self.cleaned_data['gallery']:
            logger.debug('Using pre-existing gallery.')
            gallery = self.cleaned_data['gallery']
        else:
            logger.debug(
                force_str('Creating new gallery "{0}".').format(self.cleaned_data['title']))
            gallery = create_gallery_in_site(current_site,
                                             title=self.cleaned_data['title'],
                                             description=self.cleaned_data['description'],
                                             is_public=self.cleaned_data['is_public'])

        return gallery


def create_gallery_in_site(site: Site, title: str, description: str = "", is_public: bool = False) -> Gallery:
    gallery = Gallery.objects.create(title=title,
                                     slug=slugify(title),
                                     description=description,
                                     is_public=is_public)
    gallery.sites.add(site)
    return gallery


def upload_photos_to_site(site: Site, zip: zipfile.ZipFile, gallery: Gallery, photo_defaults: PhotoDefaults)\
        -> List[UploadMessage]:
    upload_messages = []
    count = 1

    for filename in sorted(zip.namelist()):

        logger.debug(f'Reading file "{filename}".')

        if filename.startswith('__') or filename.startswith('.'):
            logger.debug(f'Ignoring file "{filename}".')
            continue

        if os.path.dirname(filename):
            logger.warning('Ignoring file "{}" as it is in a subfolder; all images should be in the top '
                           'folder of the zip.'.format(filename))
            upload_messages.append(UploadMessage.warning(
                _('Ignoring file "{filename}" as it is in a subfolder; all images should be in the top folder of the '
                  'zip.').format(filename=filename)))
            continue

        data = zip.read(filename)

        if not len(data):
            logger.debug(f'File "{filename}" is empty.')
            continue

        photo_title_root = photo_defaults.title if photo_defaults.title else gallery.title

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
                      caption=photo_defaults.caption,
                      is_public=photo_defaults.is_public)

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
            upload_messages.append(UploadMessage.warning(
                _('Could not process file "{0}" in the .zip archive.').format(filename)))
            continue

        contentfile = ContentFile(data)
        photo.image.save(filename, contentfile)
        photo.save()
        photo.sites.add(site)
        gallery.photos.add(photo)
        count += 1

    zip.close()

    upload_messages.append(UploadMessage.success(
        _('The photos have been added to gallery "{0}".').format(gallery.title)))

    return upload_messages
