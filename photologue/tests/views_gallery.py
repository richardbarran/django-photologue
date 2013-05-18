#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from photologue.tests import helpers
from photologue.tests.helpers import RequestTest

YEAR = datetime.now().year
MONTH = datetime.now().ctime().split(' ')[1].lower()
DAY = datetime.now().day

class RequestGalleryTest(RequestTest):

    def setUp(self):
        super(RequestGalleryTest, self).setUp()
        self.gallery = helpers._create_new_gallery(
            name='Fake Gallery', slug='fake-gallery')

    def tearDown(self):
        super(RequestGalleryTest, self).tearDown()
        self.gallery.delete()

    def test_archive_gallery_url_works(self):
        self.assertUrl(
            reverse('pl-gallery-archive')
        )

    def test_paginated_gallery_url_works(self):
        self.assertUrl(
            reverse('pl-gallery-list', kwargs={'page': 1})
        )

    def test_gallery_works(self):
        self.assertUrl(
            reverse('pl-gallery', kwargs={'slug': 'fake-gallery'})
        )

    def test_archive_year_gallery_works(self):
        self.assertUrl(
            reverse('pl-gallery-archive-year',
                kwargs={'year': YEAR}
            )
        )

    def test_archive_month_gallery_works(self):
        self.assertUrl(
            reverse('pl-gallery-archive-month',
                kwargs={'year': YEAR, 'month':MONTH}
            )
        )

    def test_archive_day_gallery_works(self):
        self.assertUrl(
            reverse('pl-gallery-archive-day',
                kwargs={'year': YEAR, 'month':MONTH, 'day': DAY}
            )
        )

    def test_detail_gallery_works(self):
        self.assertUrl(
            reverse('pl-gallery-detail',
                kwargs={'year': YEAR, 'month':MONTH, 'day': DAY, 'slug': 'fake-gallery'}
            )
        )

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /photologue/'), redirect them to the gallery list page."""
        response = self.client.get(reverse('pl-photologue-root'))
        self.assertRedirects(response, reverse('pl-gallery-archive'), 301, 200)


