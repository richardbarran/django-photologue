# -*- coding: utf-8 -*-
from photologue.tests.factories import PhotoFactory, PhotoSizeFactory
from django.test import TestCase

class PhotologueBaseTest(TestCase):

    def setUp(self):
        self.s = PhotoSizeFactory(name='testPhotoSize',
                                  width=100,
                                  height=100)
        self.pl = PhotoFactory(title='Landscape',
                               title_slug='landscape')

    def tearDown(self):
        # Need to manually remove the files created during testing.
        self.pl.delete()

