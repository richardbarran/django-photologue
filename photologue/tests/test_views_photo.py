from django.test import TestCase, override_settings

from ..models import Photo
from .factories import PhotoFactory


@override_settings(ROOT_URLCONF='photologue.tests.test_urls')
class RequestPhotoTest(TestCase):

    def setUp(self):
        super().setUp()
        self.photo = PhotoFactory(slug='fake-photo')

    def tearDown(self):
        super().tearDown()
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
        response = self.client.get('/ptests/photolist/')
        self.assertEqual(response.status_code, 200)

    def test_photo_works(self):
        response = self.client.get('/ptests/photo/fake-photo/')
        self.assertEqual(response.status_code, 200)

    def test_archive_year_photo_works(self):
        response = self.client.get('/ptests/photo/2011/')
        self.assertEqual(response.status_code, 200)

    def test_archive_month_photo_works(self):
        response = self.client.get('/ptests/photo/2011/12/')
        self.assertEqual(response.status_code, 200)

    def test_archive_day_photo_works(self):
        response = self.client.get('/ptests/photo/2011/12/23/')
        self.assertEqual(response.status_code, 200)

    def test_detail_photo_works(self):
        response = self.client.get('/ptests/photo/2011/12/23/fake-photo/')
        self.assertEqual(response.status_code, 200)

    def test_detail_photo_xss(self):
        """Check that the default templates handle XSS."""
        self.photo.title = '<img src=x onerror=alert("title")>'
        self.photo.caption = '<img src=x onerror=alert(origin)>'
        self.photo.save()
        response = self.client.get('/ptests/photo/2011/12/23/fake-photo/')
        self.assertContains(response, 'Photologue Demo - &lt;img src=x onerror=alert(&quot;title&quot;)&gt;')
        self.assertNotContains(response, '<img src=x onerror=alert("title")>')
        self.assertContains(response, '&lt;img src=x onerror=alert(origin)&gt;')
        self.assertNotContains(response, '<img src=x onerror=alert(origin)>')
