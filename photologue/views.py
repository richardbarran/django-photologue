#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from photologue.models import Photo, Gallery


class PhotoListView(ListView):
    queryset = Photo.objects.filter(is_public=True)
    paginate_by = 20
    allow_empty = True



class PhotoDetailView(DetailView):
    slug_field = 'title_slug'
    queryset = Photo.objects.filter(is_public=True)


class GalleryListView(ListView):
    queryset = Gallery.objects.filter(is_public=True)
    paginate_by = 20
    allow_empty = True

class GalleryDetailView(DetailView):
    slug_field = 'title_slug'
    queryset = Gallery.objects.filter(is_public=True)
