import zipfile
try:
    from zipfile import BadZipFile
except ImportError:
    # Python 2.
    from zipfile import BadZipfile as BadZipFile
import logging
import os
from io import BytesIO

try:
    import Image
except ImportError:
    from PIL import Image


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.encoding import force_text
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

from .models import Gallery, Photo

logger = logging.getLogger('photologue.forms')


class UploadZipForm(forms.Form):
    zip_file = forms.FileField()

    title = forms.CharField(label=_('Title'),
                            max_length=50,
                            required=False,
                            help_text=_('All uploaded photos will be given a title made up of this title + a '
                                        'sequential number.'))
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
                                  help_text=_('A description of this Gallery.'))
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
        cleaned_data = super(UploadZipForm, self).clean()
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
        count = 1
        current_site = Site.objects.get(id=settings.SITE_ID)
        if self.cleaned_data['gallery']:
            logger.debug('Using pre-existing gallery.')
            gallery = self.cleaned_data['gallery']
        else:
            logger.debug(
                force_text('Creating new gallery "{0}".').format(self.cleaned_data['title']))
            gallery = Gallery.objects.create(title=self.cleaned_data['title'],
                                             slug=slugify(self.cleaned_data['title']),
                                             description=self.cleaned_data['description'],
                                             is_public=self.cleaned_data['is_public'])
            gallery.sites.add(current_site)
        for filename in sorted(zip.namelist()):

            logger.debug('Reading file "{0}".'.format(filename))

            if filename.startswith('__') or filename.startswith('.'):
                logger.debug('Ignoring file "{0}".'.format(filename))
                continue

            if os.path.dirname(filename):
                logger.warning('Ignoring file "{0}" as it is in a subfolder; all images should be in the top '
                               'folder of the zip.'.format(filename))
                if request:
                    messages.warning(request,
                                     _('Ignoring file "{filename}" as it is in a subfolder; all images should '
                                       'be in the top folder of the zip.').format(filename=filename),
                                     fail_silently=True)
                continue

            data = zip.read(filename)

            if not len(data):
                logger.debug('File "{0}" is empty.'.format(filename))
                continue

            title = ' '.join([gallery.title, str(count)])
            slug = slugify(title)

            try:
                Photo.objects.get(slug=slug)
                logger.warning('Did not create photo "{0}" with slug "{1}" as a photo with that '
                               'slug already exists.'.format(filename, slug))
                if request:
                    messages.warning(request,
                                     _('Did not create photo "%(filename)s" with slug "{1}" as a photo with that '
                                       'slug already exists.').format(filename, slug),
                                     fail_silently=True)
                continue
            except Photo.DoesNotExist:
                pass

            photo = Photo(title=title,
                          slug=slug,
                          caption=self.cleaned_data['caption'],
                          is_public=self.cleaned_data['is_public'])

            # Basic check that we have a valid image.
            try:
                file = BytesIO(data)
                opened = Image.open(file)
                opened.verify()
            except Exception:
                # Pillow (or PIL) doesn't recognize it as an image.
                # If a "bad" file is found we just skip it.
                # But we do flag this both in the logs and to the user.
                logger.error('Could not process file "{0}" in the .zip archive.'.format(
                    filename))
                if request:
                    messages.warning(request,
                                     _('Could not process file "{0}" in the .zip archive.').format(
                                         filename),
                                     fail_silently=True)
                continue

            contentfile = ContentFile(data)
            photo.image.save(filename, contentfile)
            photo.save()
            photo.sites.add(current_site)
            gallery.photos.add(photo)
            count = count + 1

        zip.close()

        if request:
            messages.success(request,
                             _('The photos have been added to gallery "{0}".').format(
                                 gallery.title),
                             fail_silently=True)
