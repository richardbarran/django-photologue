import os
from django.conf import settings
from django.core.files.base import ContentFile
from photologue.models import Image, Photo, PHOTOLOGUE_DIR
from photologue.tests.helpers import LANDSCAPE_IMAGE_PATH, PhotologueBaseTest, \
QUOTING_IMAGE_PATH

class PhotoTest(PhotologueBaseTest):
    def tearDown(self):
        """Delete any extra test files (if created)."""
        super(PhotoTest, self).tearDown()
        try:
            self.pl2.delete()
        except:
            pass

    def test_new_photo(self):
        self.assertEqual(Photo.objects.count(), 1)
        self.assertTrue(os.path.isfile(self.pl.image.path))
        self.assertEqual(os.path.getsize(self.pl.image.path),
                         os.path.getsize(LANDSCAPE_IMAGE_PATH))

    #def test_exif(self):
    #    self.assertTrue(len(self.pl.EXIF.keys()) > 0)

    def test_paths(self):
        self.assertEqual(os.path.normpath(str(self.pl.cache_path())).lower(),
                         os.path.normpath(os.path.join(settings.MEDIA_ROOT,
                                      PHOTOLOGUE_DIR,
                                      'photos',
                                      'cache')).lower())
        self.assertEqual(self.pl.cache_url(),
                         settings.MEDIA_URL + PHOTOLOGUE_DIR + '/photos/cache')

    def test_count(self):
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 0)
        self.s.increment_count = True
        self.s.save()
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 5)

    def test_precache(self):
        # set the thumbnail photo size to pre-cache
        self.s.pre_cache = True
        self.s.save()
        # make sure it created the file
        self.assertTrue(os.path.isfile(self.pl.get_testPhotoSize_filename()))
        self.s.pre_cache = False
        self.s.save()
        # clear the cache and make sure the file's deleted
        self.pl.clear_cache()
        self.assertFalse(os.path.isfile(self.pl.get_testPhotoSize_filename()))

    def test_accessor_methods(self):
        self.assertEqual(self.pl.get_testPhotoSize_photosize(), self.s)
        self.assertEqual(self.pl.get_testPhotoSize_size(),
                         Image.open(self.pl.get_testPhotoSize_filename()).size)
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         self.pl.cache_url() + '/' + \
                         self.pl._get_filename_for_size(self.s))
        self.assertEqual(self.pl.get_testPhotoSize_filename(),
                         os.path.join(self.pl.cache_path(),
                         self.pl._get_filename_for_size(self.s)))

    def test_quoted_url(self):
        """Test for issue #29 - filenames of photos are incorrectly quoted when
        building a URL."""

        # Check that a 'normal' path works ok.
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         self.pl.cache_url() + '/test_photologue_landscape_testPhotoSize.jpg')

        # Now create a Photo with a name that needs quoting.
        self.pl2 = Photo(title='test', title_slug='test')
        self.pl2.image.save(os.path.basename(QUOTING_IMAGE_PATH),
                           ContentFile(open(QUOTING_IMAGE_PATH, 'rb').read()))
        self.pl2.save()
        self.assertEqual(self.pl2.get_testPhotoSize_url(),
                         self.pl2.cache_url() + '/test_photologue_%26quoting_testPhotoSize.jpg')





