from django.test import TestCase
from .factories import PhotoFactory, PhotoSizeFactory


class PhotologueBaseTest(TestCase):

    def setUp(self):
        self.s = PhotoSizeFactory(name='testPhotoSize',
                                  width=100,
                                  height=100)
        self.pl = PhotoFactory(title='Landscape',
                               slug='landscape')

    def tearDown(self):
        # Need to manually remove the files created during testing.
        self.pl.delete()
