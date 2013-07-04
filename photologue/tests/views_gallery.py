#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from photologue.tests import helpers
from photologue.models import Gallery
from django.test import TestCase

YEAR = datetime.now().year
MONTH = datetime.now().ctime().split(' ')[1].lower()
DAY = datetime.now().day

class RequestGalleryTest(TestCase):

    def setUp(self):
        super(RequestGalleryTest, self).setUp()
        self.gallery = helpers._create_new_gallery(
            name='Fake Gallery', slug='fake-gallery')

    def tearDown(self):
        super(RequestGalleryTest, self).tearDown()
        self.gallery.delete()

    def test_archive_gallery_url_works(self):
        response = self.client.get(reverse('pl-gallery-archive'))
        self.assertEqual(response.status_code, 200)

    def test_archive_gallery_empty(self):
        """If there are no galleries to show, tell the visitor - don't show a
        404."""

        Gallery.objects.all().update(is_public=False)

        response = self.client.get(reverse('pl-gallery-archive'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['latest'].count(),
                         0)

    def test_paginated_gallery_url_works(self):
        response = self.client.get(reverse('pl-gallery-list',
                                            kwargs={'page': 1}))
        self.assertEqual(response.status_code, 200)

    def test_gallery_works(self):
        response = self.client.get(reverse('pl-gallery',
                                           kwargs={'slug': 'fake-gallery'}))
        self.assertEqual(response.status_code, 200)

    def test_archive_year_gallery_works(self):
        response = self.client.get(reverse('pl-gallery-archive-year',
                                           kwargs={'year': YEAR}))
        self.assertEqual(response.status_code, 200)

    def test_archive_month_gallery_works(self):
        response = self.client.get(reverse('pl-gallery-archive-month',
                                           kwargs={'year': YEAR, 'month':MONTH}
                                           ))
        self.assertEqual(response.status_code, 200)

    def test_archive_day_gallery_works(self):
        response = self.client.get(reverse('pl-gallery-archive-day',
                                           kwargs={'year': YEAR,
                                                   'month':MONTH,
                                                   'day': DAY}))
        self.assertEqual(response.status_code, 200)

    def test_detail_gallery_works(self):
        response = self.client.get(reverse('pl-gallery-detail',
                                           kwargs={'year': YEAR,
                                                   'month':MONTH,
                                                   'day': DAY,
                                                   'slug': 'fake-gallery'}))
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /photologue/'), redirect them to the gallery list page."""
        response = self.client.get(reverse('pl-photologue-root'))
        self.assertRedirects(response, reverse('pl-gallery-archive'), 301, 200)


