#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from photologue.models import Photo, Gallery

class PhotoView(object):
    queryset = Photo.objects.filter(is_public=True)

class PhotoListView(PhotoView, ListView):
    paginate_by = 20

class PhotoDetailView(PhotoView, DetailView):
    slug_field = 'title_slug'

class PhotoDateView(PhotoView):
    date_field = 'date_added'

class PhotoDateDetailView(PhotoDateView, DateDetailView):
    slug_field = 'title_slug'

class PhotoArchiveIndexView(PhotoDateView, ArchiveIndexView):
    pass

class PhotoDayArchiveView(PhotoDateView, DayArchiveView):
    pass

class PhotoMonthArchiveView(PhotoDateView, MonthArchiveView):
    pass

class PhotoYearArchiveView(PhotoDateView, YearArchiveView):
    pass


#gallery Views
class GalleryView(object):
    queryset = Gallery.objects.filter(is_public=True)

class GalleryListView(GalleryView, ListView):
    paginate_by = 20

class GalleryDetailView(GalleryView, DetailView):
    slug_field = 'title_slug'

class GalleryDateView(GalleryView):
    date_field = 'date_added'

class GalleryDateDetailView(GalleryDateView, DateDetailView):
    slug_field = 'title_slug'

class GalleryArchiveIndexView(GalleryDateView, ArchiveIndexView):
    pass

class GalleryDayArchiveView(GalleryDateView, DayArchiveView):
    pass

class GalleryMonthArchiveView(GalleryDateView, MonthArchiveView):
    pass

class GalleryYearArchiveView(GalleryDateView, YearArchiveView):
    pass
