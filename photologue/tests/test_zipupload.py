from django.test import TestCase
from django.core.files import File

from ..models import GalleryUpload, Gallery, Photo
from .factories import SAMPLE_ZIP_PATH, SAMPLE_NOT_IMAGE_ZIP_PATH


class GalleryUploadTest(TestCase):

    def tearDown(self):
        super(GalleryUploadTest, self).tearDown()
        for photo in Photo.objects.all():
            photo.delete()

    def test_sample(self):
        """Upload a zip with a single file it it: 'sample.jpg'.
        It gets assigned to a newly created gallery 'Test Gallery'."""

        with open(SAMPLE_ZIP_PATH) as f:
            GalleryUpload.objects.create(title='Test Gallery',
                                         zip_file=File(f))

        self.assertQuerysetEqual(Gallery.objects.all(),
                                 ['<Gallery: Test Gallery>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Test Gallery 1>'])

    def test_not_image(self):
        """A zip with a file of the wrong format (.txt).
        That file gets ignored."""

        with open(SAMPLE_NOT_IMAGE_ZIP_PATH) as f:
            GalleryUpload.objects.create(title='Test Gallery',
                                         zip_file=File(f))

        self.assertQuerysetEqual(Gallery.objects.all(),
                                 ['<Gallery: Test Gallery>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Test Gallery 1>'])
