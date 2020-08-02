import zipfile
from zipfile import BadZipFile
import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .tasks import parse_zip as parse_zip_task
from .models import Gallery, ZipUploadModel
from photologue.utils.zipfile import parse_zip

logger = logging.getLogger('photologue.forms')

# Use celery to speed up page loading after uploading photos?
USE_CELERY = getattr(settings, 'PHOTOLOGUE_USE_CELERY', False)


class UploadZipForm(forms.ModelForm):
    class Meta:
        model = ZipUploadModel
        exclude = ()

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
        if USE_CELERY:
            instance = super().save(commit=False)
            instance.zip_file = zip_file
            instance.save()  # We need to save before making task to get an id
            parse_zip_task.delay(instance.id)
        else:
            parse_zip(zip_file, self.cleaned_data['gallery'], self.cleaned_data['title'],
                      self.cleaned_data['description'], self.cleaned_data['caption'], self.cleaned_data['is_public'],
                      request=request)
