#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from photologue.tests import helpers
from photologue.tests.helpers import RequestTest

YEAR = datetime.now().year
MONTH = datetime.now().ctime().split(' ')[1].lower()
DAY = datetime.now().day


class RequestPhotoTest(RequestTest):


    def setUp(self):
        super(RequestPhotoTest, self).setUp()
        self.photo = helpers._create_new_photo(name='Fake Photo', slug='fake-photo')

    def tearDown(self):
        super(RequestPhotoTest, self).tearDown()
        self.photo.delete()

    def test_archive_photo_url_works(self):
        self.assertUrl(
            reverse('pl-photo-archive')
        )

    def test_paginated_photo_url_works(self):
        self.assertUrl(
            reverse('pl-photo-list', kwargs={'page': 1})
        )

    def test_photo_works(self):
        self.assertUrl(
            reverse('pl-photo', kwargs={'slug': 'fake-photo'})
        )


    def test_archive_year_photo_works(self):
        self.assertUrl(
            reverse('pl-photo-archive-year', kwargs={'year': YEAR})
        )

    def test_archive_month_photo_works(self):
        self.assertUrl(
            reverse('pl-photo-archive-month', kwargs={'year': YEAR, 'month':MONTH})
        )

    def test_archive_day_photo_works(self):
        self.assertUrl(
            reverse('pl-photo-archive-day', kwargs={'year': YEAR, 'month':MONTH, 'day': DAY})
        )


    def test_detail_photo_works(self):
        self.assertUrl(
            reverse('pl-photo-detail', kwargs={'year': YEAR, 'month':MONTH, 'day': DAY, 'slug': 'fake-photo'})
        )
