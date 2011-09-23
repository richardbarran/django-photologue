# -*- coding: utf-8 -*-
from django.core.files.base import ContentFile
import os
from photologue.models import PhotoSize, Photo
from django.test import TestCase

RES_DIR = os.path.join(os.path.dirname(__file__), '../res')
LANDSCAPE_IMAGE_PATH = os.path.join(RES_DIR, 'test_landscape.jpg')
PORTRAIT_IMAGE_PATH = os.path.join(RES_DIR, 'test_portrait.jpg')
SQUARE_IMAGE_PATH = os.path.join(RES_DIR, 'test_square.jpg')


class PhotologueBaseTest(TestCase):
    def setUp(self):
        self.s = PhotoSize(name='test', width=100, height=100)
        self.s.save()
        self.pl = Photo(title='landscape', title_slug='landscape')
        self.pl.image.save(os.path.basename(LANDSCAPE_IMAGE_PATH),
                           ContentFile(open(LANDSCAPE_IMAGE_PATH, 'rb').read()))
        self.pl.save()

    def tearDown(self):
        self.pl.delete()
        self.s.delete()

