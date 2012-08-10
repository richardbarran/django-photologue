import Image
import os
from django.conf import settings
from django.core.files.base import ContentFile
from photologue.models import Photo, PHOTOLOGUE_DIR, PhotoSizeCache, PhotoEffect
from photologue.tests.helpers import LANDSCAPE_IMAGE_PATH, PORTRAIT_IMAGE_PATH, SQUARE_IMAGE_PATH, PhotologueBaseTest


class PhotoTest(PhotologueBaseTest):
    def test_new_photo(self):
        self.assertEqual(Photo.objects.count(), 1)
        self.assertTrue(os.path.isfile(self.pl.image.path))
        self.assertEqual(os.path.getsize(self.pl.image.path),
                         os.path.getsize(LANDSCAPE_IMAGE_PATH))

    #def test_exif(self):
    #    self.assert_(len(self.pl.EXIF.keys()) > 0)

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
            self.pl.get_test_url()
        self.assertEquals(self.pl.view_count, 0)
        self.s.increment_count = True
        self.s.save()
        for i in range(5):
            self.pl.get_test_url()
        self.assertEquals(self.pl.view_count, 5)

    def test_precache(self):
        # set the thumbnail photo size to pre-cache
        self.s.pre_cache = True
        self.s.save()
        # make sure it created the file
        self.assertTrue(os.path.isfile(self.pl.get_test_filename()))
        self.s.pre_cache = False
        self.s.save()
        # clear the cache and make sure the file's deleted
        self.pl.clear_cache()
        self.assertFalse(os.path.isfile(self.pl.get_test_filename()))

    def test_accessor_methods(self):
        self.assertEquals(self.pl.get_test_photosize(), self.s)
        self.assertEquals(self.pl.get_test_size(),
                          Image.open(self.pl.get_test_filename()).size)
        self.assertEquals(self.pl.get_test_url(),
                          self.pl.cache_url() + '/' + \
                          self.pl._get_filename_for_size(self.s))
        self.assertEquals(self.pl.get_test_filename(),
                          os.path.join(self.pl.cache_path(),
                          self.pl._get_filename_for_size(self.s)))







