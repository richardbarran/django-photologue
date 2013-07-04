#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from photologue.tests import helpers
from photologue.models import Photo
from django.test import TestCase

YEAR = datetime.now().year
MONTH = datetime.now().ctime().split(' ')[1].lower()
DAY = datetime.now().day


class RequestPhotoTest(TestCase):


    def setUp(self):
        super(RequestPhotoTest, self).setUp()
        self.photo = helpers._create_new_photo(name='Fake Photo', slug='fake-photo')

    def tearDown(self):
        super(RequestPhotoTest, self).tearDown()
        self.photo.delete()

    def test_archive_photo_url_works(self):
        response = self.client.get(reverse('pl-photo-archive'))
        self.assertEqual(response.status_code, 200)

    def test_archive_photo_empty(self):
        """If there are no photo to show, tell the visitor - don't show a
        404."""

        Photo.objects.all().update(is_public=False)

        response = self.client.get(reverse('pl-photo-archive'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['latest'].count(),
                         0)


    def test_paginated_photo_url_works(self):
        response = self.client.get(reverse('pl-photo-list', kwargs={'page': 1}))
        self.assertEqual(response.status_code, 200)

    def test_photo_works(self):
        response = self.client.get(reverse('pl-photo',
                                           kwargs={'slug': 'fake-photo'}))
        self.assertEqual(response.status_code, 200)


    def test_archive_year_photo_works(self):
        response = self.client.get(reverse('pl-photo-archive-year',
                                           kwargs={'year': YEAR}))
        self.assertEqual(response.status_code, 200)

    def test_archive_month_photo_works(self):
        response = self.client.get(reverse('pl-photo-archive-month',
                                          kwargs={'year': YEAR, 'month':MONTH}))
        self.assertEqual(response.status_code, 200)

    def test_archive_day_photo_works(self):
        response = self.client.get(reverse('pl-photo-archive-day',
                                           kwargs={'year': YEAR,
                                                   'month':MONTH,
                                                   'day': DAY}))
        self.assertEqual(response.status_code, 200)


    def test_detail_photo_works(self):
        response = self.client.get(reverse('pl-photo-detail',
                                           kwargs={'year': YEAR,
                                                   'month':MONTH,
                                                   'day': DAY,
                                                   'slug': 'fake-photo'}))
        self.assertEqual(response.status_code, 200)
