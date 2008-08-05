import os
import unittest
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from models import *

# Path to sample image
RES_DIR = os.path.join(os.path.dirname(__file__), 'res')
LANDSCAPE_IMAGE_PATH = os.path.join(RES_DIR, 'test_landscape.jpg')
PORTRAIT_IMAGE_PATH = os.path.join(RES_DIR, 'test_portrait.jpg')
SQUARE_IMAGE_PATH = os.path.join(RES_DIR, 'test_square.jpg')


class TestUploadedFile(InMemoryUploadedFile):
    """ Simplified uploadedfile wrapper
    
    Django's save_FIELD_file method expects an object that has the method
    "chunks" so we need to pass the file data in the appropriate wrapper.
    """
    def __init__(self, file):
        self.file = file
        self.field_name = None
        self.file.seek(0)
        
        
class TestPhoto(ImageModel):
    """ Minimal ImageModel class for testing """
    name = models.CharField(max_length=30)
    
    
class PLTest(TestCase):
    """ Base TestCase class """
    def setUp(self):
        self.s = PhotoSize(name='test', width=100, height=100)
        self.s.save()
        self.pl = TestPhoto(name='landscape')
        self.pl.save_image_file(os.path.basename(LANDSCAPE_IMAGE_PATH),
                               TestUploadedFile(open(LANDSCAPE_IMAGE_PATH, 'rb')))
        self.pl.save()

    def tearDown(self):
        self.pl.delete()
        self.failIf(os.path.isfile(self.pl.get_image_filename()))
        self.s.delete()     


class PhotoTest(PLTest):    
    def test_new_photo(self):
        self.assertEqual(TestPhoto.objects.count(), 1)
        self.failUnless(os.path.isfile(self.pl.get_image_filename()))
        self.assertEqual(os.path.getsize(self.pl.get_image_filename()),
                                         os.path.getsize(LANDSCAPE_IMAGE_PATH))
                                         
    def test_exif(self):
        self.assert_(len(self.pl.EXIF.keys()) > 0)

    def test_paths(self):
        self.assertEqual(os.path.normpath(self.pl.cache_path()),
                         os.path.normpath(os.path.join(settings.MEDIA_ROOT,
                                      PHOTOLOGUE_DIR,
                                      'photos',
                                      'cache')))
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
        self.failUnless(os.path.isfile(self.pl.get_test_filename()))
        self.s.pre_cache = False
        self.s.save()
        # clear the cache and make sure the file's deleted
        self.pl.clear_cache()
        self.failIf(os.path.isfile(self.pl.get_test_filename()))
        
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
        
        
class ImageResizeTest(PLTest):
    def setUp(self):
        super(ImageResizeTest, self).setUp()
        self.pp = TestPhoto(name='portrait')
        self.pp.save_image_file(os.path.basename(PORTRAIT_IMAGE_PATH),
                               TestUploadedFile(open(PORTRAIT_IMAGE_PATH, 'rb')))
        self.pp.save()
        self.ps = TestPhoto(name='square')
        self.ps.save_image_file(os.path.basename(SQUARE_IMAGE_PATH),
                               TestUploadedFile(open(SQUARE_IMAGE_PATH, 'rb')))
        self.ps.save()
        
    def tearDown(self):
        super(ImageResizeTest, self).tearDown()
        self.pp.delete()
        self.ps.delete()
             
    def test_resize_to_fit(self):
        self.assertEquals(self.pl.get_test_size(), (100, 75))
        self.assertEquals(self.pp.get_test_size(), (75, 100))
        self.assertEquals(self.ps.get_test_size(), (100, 100))
        
    def test_resize_to_fit_width(self):
        self.s.size = (100, 0)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (100, 75))
        self.assertEquals(self.pp.get_test_size(), (100, 133))
        self.assertEquals(self.ps.get_test_size(), (100, 100))
        
    def test_resize_to_fit_width_enlarge(self):
        self.s.size = (2000, 0)
        self.s.upscale = True
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (2000, 1500))
        self.assertEquals(self.pp.get_test_size(), (2000, 2667))
        self.assertEquals(self.ps.get_test_size(), (2000, 2000))

    def test_resize_to_fit_height(self):
        self.s.size = (0, 100)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (133, 100))
        self.assertEquals(self.pp.get_test_size(), (75, 100))
        self.assertEquals(self.ps.get_test_size(), (100, 100))
        
    def test_resize_to_fit_height_enlarge(self):
        self.s.size = (0, 2000)
        self.s.upscale = True
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (2667, 2000))
        self.assertEquals(self.pp.get_test_size(), (1500, 2000))
        self.assertEquals(self.ps.get_test_size(), (2000, 2000))
        
    def test_resize_and_crop(self):
        self.s.crop = True
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), self.s.size)
        self.assertEquals(self.pp.get_test_size(), self.s.size)
        self.assertEquals(self.ps.get_test_size(), self.s.size)
        
    def test_resize_rounding_to_fit(self):
        self.s.size = (113, 113)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (113, 85))
        self.assertEquals(self.pp.get_test_size(), (85, 113))
        self.assertEquals(self.ps.get_test_size(), (113, 113))  
        
    def test_resize_rounding_cropped(self):
        self.s.size = (113, 113)
        self.s.crop = True
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), self.s.size)
        self.assertEquals(self.pp.get_test_size(), self.s.size)
        self.assertEquals(self.ps.get_test_size(), self.s.size)
        
    def test_resize_one_dimension_width(self):
        self.s.size = (1500, 1200)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (1500, 1125))
        
    def test_resize_one_dimension_height(self):
        self.s.size = (1600, 1100)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (1467, 1100))
        
    def test_resize_no_upscale(self):
        self.s.size = (2000, 2000)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (1600, 1200))
        
    def test_resize_no_upscale_mixed_height(self):
        self.s.size = (3200, 600)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (800, 600))
        
    def test_resize_no_upscale_mixed_width(self):
        self.s.size = (800, 2400)
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (800, 600))
        
    def test_resize_no_upscale_crop(self):
        self.s.size = (2000, 2000)
        self.s.crop = True
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (2000, 2000))
        
    def test_resize_upscale(self):
        self.s.size = (2000, 2000)
        self.s.upscale = True
        self.s.save()
        self.assertEquals(self.pl.get_test_size(), (2000, 1500))
        self.assertEquals(self.pp.get_test_size(), (1500, 2000))
        self.assertEquals(self.ps.get_test_size(), (2000, 2000))


class PhotoEffectTest(PLTest):
    def test(self):
        effect = PhotoEffect(name='test')
        im = Image.open(self.pl.get_image_filename())
        self.assert_(isinstance(effect.pre_process(im), Image.Image))
        self.assert_(isinstance(effect.post_process(im), Image.Image))
        self.assert_(isinstance(effect.process(im), Image.Image))


class PhotoSizeCacheTest(PLTest):
    def test(self):
        cache = PhotoSizeCache()
        self.assertEqual(cache.sizes['test'], self.s)    
        
