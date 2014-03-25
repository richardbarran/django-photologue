from django.test import TestCase
from django.contrib.sites.models import Site

from .factories import GalleryFactory, PhotoFactory


class SitesTest(TestCase):

    urls = 'photologue.tests.test_urls'

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

        self.gallery1 = GalleryFactory(slug='test-gallery')
        self.gallery2 = GalleryFactory(slug='not-on-site-gallery')
        self.photo1 = PhotoFactory(slug='test-photo')
        self.photo2 = PhotoFactory(slug='not-on-site-photo')
        self.gallery1.photos.add(self.photo1, self.photo2)

        # I'd like to use factory_boy's mute_signal decorator but that
        # will only available once factory_boy 2.4 is released. So long
        # we'll have to remove the site association manually
        self.gallery2.sites.clear()
        self.photo2.sites.clear()

    def tearDown(self):
        super(SitesTest, self).tearDown()
        self.gallery1.delete()
        self.gallery2.delete()
        self.photo1.delete()
        self.photo2.delete()

    def test_basics(self):
        """ See if objects were added automatically to the current site. """
        self.assertEqual(list(self.gallery1.sites.all()), [self.site1])
        self.assertEqual(list(self.photo1.sites.all()), [self.site1])

    def test_empty_sites(self):
        """
        Objects should not be associated with a particular site when
        ``PHOTOLOGUE_ADD_DEFAULT_SITE`` is ``False``.
        """
        with self.settings(PHOTOLOGUE_ADD_DEFAULT_SITE=False):
            self.gallery2 = GalleryFactory()
            self.photo2 = PhotoFactory(slug='test-photo2')
            self.assertEqual(list(self.gallery2.sites.all()), [])
            self.assertEqual(list(self.photo2.sites.all()), [])

    def test_gallery_list(self):
        response = self.client.get('/ptests/gallery/page/1/')
        self.assertEqual(list(response.context['object_list']), [self.gallery1])

    def test_gallery_detail(self):
        response = self.client.get('/ptests/gallery/test-gallery/')
        self.assertEqual(response.context['object'], self.gallery1)

        response = self.client.get('/ptests/gallery/not-on-site-gallery/')
        self.assertEqual(response.status_code, 404)

    def test_photo_list(self):
        response = self.client.get('/ptests/photo/page/1/')
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
