from django.test import TestCase
from .factories import PhotoFactory
from ..models import Photo


class RequestPhotoTest(TestCase):

    urls = 'photologue.tests.test_urls'

    def setUp(self):
        super(RequestPhotoTest, self).setUp()
        self.photo = PhotoFactory(title_slug='fake-photo')

    def tearDown(self):
        super(RequestPhotoTest, self).tearDown()
        self.photo.delete()

    def test_archive_photo_url_works(self):
        response = self.client.get('/ptests/photo/')
        self.assertEqual(response.status_code, 200)

    def test_archive_photo_empty(self):
        """If there are no photo to show, tell the visitor - don't show a
        404."""

        Photo.objects.all().update(is_public=False)

        response = self.client.get('/ptests/photo/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['latest'].count(),
                         0)

    def test_paginated_photo_url_works(self):
        response = self.client.get('/ptests/photo/page/1/')
        self.assertEqual(response.status_code, 200)

    def test_photo_works(self):
        response = self.client.get('/ptests/photo/fake-photo/')
        self.assertEqual(response.status_code, 200)

    def test_archive_year_photo_works(self):
        response = self.client.get('/ptests/photo/2011/')
        self.assertEqual(response.status_code, 200)

    def test_archive_month_photo_works(self):
        response = self.client.get('/ptests/photo/2011/dec/')
        self.assertEqual(response.status_code, 200)

    def test_archive_day_photo_works(self):
        response = self.client.get('/ptests/photo/2011/dec/23/')
        self.assertEqual(response.status_code, 200)

    def test_detail_photo_works(self):
        response = self.client.get('/ptests/photo/2011/dec/23/fake-photo/')
        self.assertEqual(response.status_code, 200)


class PhotoPaginationTest(TestCase):

    urls = 'photologue.tests.test_urls'

    def test_pagination(self):
        photos = []
        for i in range(1, 23):
            photos.append(
                PhotoFactory(title='photo{0:0>3}'.format(i))
            )

        response = self.client.get('/ptests/photo/page/1/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']),
                         20)
        # Check first and last items.
        self.assertEqual(response.context['object_list'][0].title,
                         'photo022')
        self.assertEqual(response.context['object_list'][19].title,
                         'photo003')

        # Now get the second page of results.
        response = self.client.get('/ptests/photo/page/2/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']),
                         2)
        # Check first and last items.
        self.assertEqual(response.context['object_list'][0].title,
                         'photo002')
        self.assertEqual(response.context['object_list'][1].title,
                         'photo001')

        # Need to clean up and manually remove all photos.
        for photo in photos:
            photo.delete()
