#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from photologue.models import Photo, Gallery

class PhotoView(object):
    queryset = Photo.objects.filter(is_public=True)


class GalleryView(object):
    queryset = Gallery.objects.filter(is_public=True)


class PhotoListView(PhotoView, ListView):
    paginate_by = 20
    allow_empty = True


class PhotoDetailView(PhotoView, DetailView):
    slug_field = 'title_slug'


class GalleryListView(GalleryView, ListView):
    paginate_by = 20
    allow_empty = True

class GalleryDetailView(GalleryView, DetailView):
    slug_field = 'title_slug'
