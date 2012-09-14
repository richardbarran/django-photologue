# -*- coding: utf-8 -*-
from django.core.files.base import ContentFile
from django.test.client import Client
import os
from photologue.models import PhotoSize, Photo, Gallery
from django.test import TestCase

RES_DIR = os.path.join(os.path.dirname(__file__), '../res')
LANDSCAPE_IMAGE_PATH = os.path.join(RES_DIR, 'test_landscape.jpg')
PORTRAIT_IMAGE_PATH = os.path.join(RES_DIR, 'test_portrait.jpg')
SQUARE_IMAGE_PATH = os.path.join(RES_DIR, 'test_square.jpg')
QUOTING_IMAGE_PATH = os.path.join(RES_DIR, 'test_&quoting.jpg')

def _create_new_photo(name, slug):
    pl = Photo(title=name, title_slug=slug)
    pl.image.save(os.path.basename(LANDSCAPE_IMAGE_PATH),
                       ContentFile(open(LANDSCAPE_IMAGE_PATH, 'rb').read()))
    pl.save()
    return pl

class RequestTest(TestCase):

    def setUp(self):
        self.client = Client()

    def assertUrl(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class PhotologueBaseTest(TestCase):

    def setUp(self):
        self.s = PhotoSize(name='testPhotoSize', width=100, height=100)
        self.s.save()
        self.pl = _create_new_photo(name='Landscape', slug='landscape')

    def tearDown(self):
        self.pl.delete()
        self.s.delete()


def _create_new_gallery(name, slug):
    gallery = Gallery.objects.create(title=name, title_slug=slug)
    return gallery
