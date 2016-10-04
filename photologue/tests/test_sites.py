import unittest

from django.test import TestCase, override_settings
from django.contrib.sites.models import Site
from django.conf import settings

from .factories import GalleryFactory, PhotoFactory


@override_settings(ROOT_URLCONF='photologue.tests.test_urls')
class SitesTest(TestCase):

    def setUp(self):
        """
        Create two example sites that we can use to test what gets displayed
        where.
        """
        super(SitesTest, self).setUp()

        self.site1, created1 = Site.objects.get_or_create(
            domain="example.com", name="example.com")
        self.site2, created2 = Site.objects.get_or_create(
            domain="example.org", name="example.org")

        with self.settings(PHOTOLOGUE_MULTISITE=True):
            # Be explicit about linking Galleries/Photos to Sites."""
            self.gallery1 = GalleryFactory(slug='test-gallery', sites=[self.site1])
            self.gallery2 = GalleryFactory(slug='not-on-site-gallery')
            self.photo1 = PhotoFactory(slug='test-photo', sites=[self.site1])
            self.photo2 = PhotoFactory(slug='not-on-site-photo')
            self.gallery1.photos.add(self.photo1, self.photo2)

        # I'd like to use factory_boy's mute_signal decorator but that
        # will only available once factory_boy 2.4 is released. So long
        # we'll have to remove the site association manually
        self.photo2.sites.clear()

    def tearDown(self):
        super(SitesTest, self).tearDown()
        self.gallery1.delete()
        self.gallery2.delete()
        self.photo1.delete()
        self.photo2.delete()

    def test_basics(self):
        """ See if objects were added automatically (by the factory) to the current site. """
        self.assertEqual(list(self.gallery1.sites.all()), [self.site1])
        self.assertEqual(list(self.photo1.sites.all()), [self.site1])

    def test_auto_add_sites(self):
        """
        Objects should not be automatically associated with a particular site when
        ``PHOTOLOGUE_MULTISITE`` is ``True``.
        """

        with self.settings(PHOTOLOGUE_MULTISITE=False):
            gallery = GalleryFactory()
            photo = PhotoFactory()
        self.assertEqual(list(gallery.sites.all()), [self.site1])
        self.assertEqual(list(photo.sites.all()), [self.site1])

        photo.delete()

        with self.settings(PHOTOLOGUE_MULTISITE=True):
            gallery = GalleryFactory()
            photo = PhotoFactory()
        self.assertEqual(list(gallery.sites.all()), [])
        self.assertEqual(list(photo.sites.all()), [])

        photo.delete()

    def test_gallery_list(self):
        response = self.client.get('/ptests/gallerylist/')
        self.assertEqual(list(response.context['object_list']), [self.gallery1])

    def test_gallery_detail(self):
        response = self.client.get('/ptests/gallery/test-gallery/')
        self.assertEqual(response.context['object'], self.gallery1)

        response = self.client.get('/ptests/gallery/not-on-site-gallery/')
        self.assertEqual(response.status_code, 404)

    def test_photo_list(self):
        response = self.client.get('/ptests/photolist/')
        self.assertEqual(list(response.context['object_list']), [self.photo1])

    def test_photo_detail(self):
        response = self.client.get('/ptests/photo/test-photo/')
        self.assertEqual(response.context['object'], self.photo1)

        response = self.client.get('/ptests/photo/not-on-site-photo/')
        self.assertEqual(response.status_code, 404)

    def test_photo_archive(self):
        response = self.client.get('/ptests/photo/')
        self.assertEqual(list(response.context['object_list']), [self.photo1])

    def test_photos_in_gallery(self):
        """
        Only those photos are supposed to be shown in a gallery that are
        also associated with the current site.
        """
        response = self.client.get('/ptests/gallery/test-gallery/')
        self.assertEqual(list(response.context['object'].public()), [self.photo1])

    @unittest.skipUnless('django.contrib.sitemaps' in settings.INSTALLED_APPS,
                         'Sitemaps not installed in this project, nothing to test.')
    def test_sitemap(self):
        """A sitemap should only show objects associated with the current site."""
        response = self.client.get('/sitemap.xml')

        # Check photos.
        self.assertContains(response,
                            '<url><loc>http://example.com/ptests/photo/test-photo/</loc>'
                            '<lastmod>2011-12-23</lastmod></url>')
        self.assertNotContains(response,
                               '<url><loc>http://example.com/ptests/photo/not-on-site-photo/</loc>'
                               '<lastmod>2011-12-23</lastmod></url>')

        # Check galleries.
        self.assertContains(response,
                            '<url><loc>http://example.com/ptests/gallery/test-gallery/</loc>'
                            '<lastmod>2011-12-23</lastmod></url>')
        self.assertNotContains(response,
                               '<url><loc>http://example.com/ptests/gallery/not-on-site-gallery/</loc>'
                               '<lastmod>2011-12-23</lastmod></url>')

    def test_orphaned_photos(self):
        self.assertEqual(list(self.gallery1.orphaned_photos()), [self.photo2])

        self.gallery2.photos.add(self.photo2)
        self.assertEqual(list(self.gallery1.orphaned_photos()), [self.photo2])

        self.gallery1.sites.clear()
        self.assertEqual(list(self.gallery1.orphaned_photos()), [self.photo1, self.photo2])

        self.photo1.sites.clear()
        self.photo2.sites.clear()
        self.assertEqual(list(self.gallery1.orphaned_photos()), [self.photo1, self.photo2])
