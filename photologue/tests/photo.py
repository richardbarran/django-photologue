import os
from django.conf import settings
from django.core.files.base import ContentFile
from imagekit.cachefiles import ImageCacheFile
from photologue.models import Image, Photo, PHOTOLOGUE_DIR
from photologue.processors import PhotologueSpec
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

    def test_accessor_methods_photosize(self):
        self.assertEqual(self.pl.get_testPhotoSize_photosize(), self.s)

    def test_accessor_methods_size(self):
        self.assertEqual(self.pl.get_testPhotoSize_size(),
                         Image.open(self.pl.get_testPhotoSize_filename()).size)

    def test_accessor_methods_url(self):
        generator = PhotologueSpec(photo=self.pl, photosize=self.s)
        cache = ImageCacheFile(generator)
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         cache.url)


    def test_accessor_methods_filename(self):
        generator = PhotologueSpec(photo=self.pl, photosize=self.s)
        cache = ImageCacheFile(generator)
        self.assertEqual(self.pl.get_testPhotoSize_filename(), cache.file.name)


    def test_quoted_url(self):
        """Test for issue #29 - filenames of photos are incorrectly quoted when
        building a URL."""
        generator = PhotologueSpec(photo=self.pl, photosize=self.s)
        cache = ImageCacheFile(generator)

        # Check that a 'normal' path works ok.
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         cache.url)

        # Now create a Photo with a name that needs quoting.
        self.pl2 = Photo(title='test', title_slug='test')
        self.pl2.image.save(os.path.basename(QUOTING_IMAGE_PATH),
                           ContentFile(open(QUOTING_IMAGE_PATH, 'rb').read()))
        self.pl2.save()

        generator = PhotologueSpec(photo=self.pl2, photosize=self.s)
        cache = ImageCacheFile(generator)

        self.assertEqual(self.pl2.get_testPhotoSize_url(),
                         cache.url)






