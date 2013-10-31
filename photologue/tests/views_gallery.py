from django.test import TestCase
from .factories import GalleryFactory


class RequestGalleryTest(TestCase):

    urls = 'photologue.tests.test_urls'

    def setUp(self):
        super(RequestGalleryTest, self).setUp()
        self.gallery = GalleryFactory(title_slug='test-gallery')

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
        response = self.client.get('/ptests/gallery/page/1/')
        self.assertEqual(response.status_code, 200)

    def test_gallery_works(self):
        response = self.client.get('/ptests/gallery/test-gallery/')
        self.assertEqual(response.status_code, 200)

    def test_archive_year_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/')
        self.assertEqual(response.status_code, 200)

    def test_archive_month_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/dec/')
        self.assertEqual(response.status_code, 200)

    def test_archive_day_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/dec/23/')
        self.assertEqual(response.status_code, 200)

    def test_detail_gallery_works(self):
        response = self.client.get('/ptests/gallery/2011/dec/23/test-gallery/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /ptests/'), redirect them to the gallery list page."""
        response = self.client.get('/ptests/')
        self.assertRedirects(response, '/ptests/gallery/', 301, 200)


class GalleryPaginationTest(TestCase):

    urls = 'photologue.tests.test_urls'

    def test_pagination(self):
        for i in range(1, 23):
            GalleryFactory(title='gallery{0:0>3}'.format(i))

        response = self.client.get('/ptests/gallery/page/1/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']),
                         20)
        # Check first and last items.
        self.assertEqual(response.context['object_list'][0].title,
                         'gallery022')
        self.assertEqual(response.context['object_list'][19].title,
                         'gallery003')

        # Now get the second page of results.
        response = self.client.get('/ptests/gallery/page/2/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']),
                         2)
        # Check first and last items.
        self.assertEqual(response.context['object_list'][0].title,
                         'gallery002')
        self.assertEqual(response.context['object_list'][1].title,
                         'gallery001')
