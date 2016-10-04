from django.test import TestCase, override_settings
from .factories import GalleryFactory


@override_settings(ROOT_URLCONF='photologue.tests.test_urls')
class RequestGalleryTest(TestCase):

    def setUp(self):
        super(RequestGalleryTest, self).setUp()
        self.gallery = GalleryFactory(slug='test-gallery')

    def test_archive_gallery_url_works(self):
        response = self.client.get('/ptests/gallery/')
        self.assertEqual(response.status_code, 200)

    def test_archive_gallery_empty(self):
        """If there are no galleries to show, tell the visitor - don't show a
        404."""

        self.gallery.is_public = False
        self.gallery.save()

        response = self.client.get('/ptests/gallery/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['latest'].count(),
                         0)

    def test_paginated_gallery_url_works(self):
        response = self.client.get('/ptests/gallerylist/')
        self.assertEqual(response.status_code, 200)

    def test_gallery_works(self):
        response = self.client.get('/ptests/gallery/test-gallery/')
        self.assertEqual(response.status_code, 200)

    def test_archive_year_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/')
        self.assertEqual(response.status_code, 200)

    def test_archive_month_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/12/')
        self.assertEqual(response.status_code, 200)

    def test_archive_day_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/12/23/')
        self.assertEqual(response.status_code, 200)

    def test_detail_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/12/23/test-gallery/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /ptests/'), redirect them to the gallery list page."""
        response = self.client.get('/ptests/')
        self.assertRedirects(response, '/ptests/gallery/', 301, 200)
