from django.conf import settings
from django.utils import unittest

from photologue.tests import helpers
from .factories import GalleryFactory

import datetime

@unittest.skipUnless('django.contrib.sitemaps' in settings.INSTALLED_APPS,
                     'Sitemaps not installed in this project, nothing to test.')
class SitemapTest(helpers.PhotologueBaseTest):

    urls = 'photologue.tests.test_urls'

    def test_get_photo(self):
        """Default test setup contains one photo, this should appear in the sitemap."""
        response = self.client.get('/sitemap.xml')
        today = datetime.date.today().strftime('%Y-%m-%d')
        photo_string = '<url><loc>http://example.com/ptests/photo/landscape/</loc><lastmod>{today}</lastmod><priority>0.5</priority></url>'\
                       .format(today=today)
        self.assertContains(response, photo_string)

    def test_get_gallery(self):
        """if we add a gallery to the site, we should see both the gallery and
        the photo in the sitemap."""
        self.gallery = GalleryFactory(title_slug='test-gallery')

        response = self.client.get('/sitemap.xml')
        today = datetime.date.today().strftime('%Y-%m-%d')
        photo_string = '<url><loc>http://example.com/ptests/photo/landscape/</loc><lastmod>{today}</lastmod><priority>0.5</priority></url>'\
                       .format(today=today)
        self.assertContains(response, photo_string)

        gallery_string = '<url><loc>http://example.com/ptests/gallery/test-gallery/</loc><lastmod>{today}</lastmod><priority>0.5</priority></url>'\
                       .format(today=today)
        self.assertContains(response, gallery_string)

