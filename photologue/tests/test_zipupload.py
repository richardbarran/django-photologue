from django.test import TestCase
from django.core.files import File
from django.core.exceptions import ValidationError

from ..models import GalleryUpload, Gallery, Photo
from .factories import GalleryFactory, PhotoFactory, SAMPLE_ZIP_PATH, SAMPLE_NOT_IMAGE_ZIP_PATH, \
    IGNORED_FILES_ZIP_PATH


class GalleryUploadTest(TestCase):

    def tearDown(self):
        super(GalleryUploadTest, self).tearDown()
        for photo in Photo.objects.all():
            photo.delete()

    def test_sample(self):
        """Upload a zip with a single file it it: 'sample.jpg'.
        It gets assigned to a newly created gallery 'Test'."""

        with open(SAMPLE_ZIP_PATH, mode='rb') as f:
            test_file = File(f)
            GalleryUpload.objects.create(title='Test',
                                         zip_file=test_file)

        self.assertQuerysetEqual(Gallery.objects.all(),
                                 ['<Gallery: Test>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Test 1>'])

        # The photo is attached to the gallery.
        gallery = Gallery.objects.get(title='Test')
        self.assertQuerysetEqual(gallery.photos.all(),
                                 ['<Photo: Test 1>'])

    def test_not_image(self):
        """A zip with a file of the wrong format (.txt).
        That file gets ignored."""

        with open(SAMPLE_NOT_IMAGE_ZIP_PATH, mode='rb') as f:
            test_file = File(f)
            GalleryUpload.objects.create(title='Test',
                                         zip_file=test_file)

        self.assertQuerysetEqual(Gallery.objects.all(),
                                 ['<Gallery: Test>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Test 1>'])

    def test_ignored(self):
        """Ignore anything that does not look like a image file.
        E.g. hidden files, and folders.
        We have two images: one in the top level of the zip, and one in a subfolder.
        The second one gets ignored - we only process files at the zip root."""

        with open(IGNORED_FILES_ZIP_PATH, mode='rb') as f:
            test_file = File(f)
            GalleryUpload.objects.create(title='Test',
                                         zip_file=test_file)

        self.assertQuerysetEqual(Gallery.objects.all(),
                                 ['<Gallery: Test>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Test 1>'])

    def test_existing(self):
        """Add the photos in the zip to an existing gallery."""

        existing = GalleryFactory(title='Existing')

        with open(SAMPLE_ZIP_PATH, mode='rb') as f:
            test_file = File(f)
            # Note how the title is not required.
            GalleryUpload.objects.create(zip_file=test_file,
                                         gallery=existing)

        self.assertQuerysetEqual(Gallery.objects.all(),
                                 ['<Gallery: Existing>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Existing 1>'])

        # The photo is attached to the existing gallery.
        self.assertQuerysetEqual(existing.photos.all(),
                                 ['<Photo: Existing 1>'])

    def test_duplicate_gallery(self):
        """If we try to create Gallery with a title
        that duplicates an existing title, refuse to load."""

        GalleryFactory(title='Test')

        with open(SAMPLE_ZIP_PATH, mode='rb') as f:
            test_file = File(f)
            gallery = GalleryUpload(title='Test',
                                    zip_file=test_file)
        self.assertRaisesMessage(ValidationError,
                                 'A gallery with that title already exists.',
                                 gallery.clean)

    def test_title_or_gallery(self):
        """We should supply either a title field or a gallery."""

        gallery = GalleryUpload()
        self.assertRaisesMessage(ValidationError,
                                 'Select an existing gallery or enter a new gallery name.',
                                 gallery.clean)

    def test_duplicate_title(self):
        """If we try to create a Photo from the archive with a title
        that duplicates an existing title, raise a warning."""

        PhotoFactory(title='Test 1')

        with open(SAMPLE_ZIP_PATH, mode='rb') as f:
            test_file = File(f)
            GalleryUpload.objects.create(title='Test',
                                         zip_file=test_file)

        self.assertQuerysetEqual(Gallery.objects.all(),
                                 ['<Gallery: Test>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Test 1>'])

        # The (existing) photo is NOT attached to the gallery.
        gallery = Gallery.objects.get(title='Test')
        self.assertQuerysetEqual(gallery.photos.all(),
                                 [])
