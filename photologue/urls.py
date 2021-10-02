from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView

from .views import (GalleryArchiveIndexView, GalleryDateDetailView, GalleryDayArchiveView, GalleryDetailView,
                    GalleryListView, GalleryMonthArchiveView, GalleryYearArchiveView, PhotoArchiveIndexView,
                    PhotoDateDetailView, PhotoDayArchiveView, PhotoDetailView, PhotoListView, PhotoMonthArchiveView,
                    PhotoYearArchiveView)

"""NOTE: the url names are changing. In the long term, I want to remove the 'pl-'
prefix on all urls, and instead rely on an application namespace 'photologue'.

At the same time, I want to change some URL patterns, e.g. for pagination. Changing the urls
twice within a few releases, could be confusing, so instead I am updating URLs bit by bit.

The new style will coexist with the existing 'pl-' prefix for a couple of releases.

"""

app_name = 'photologue'
urlpatterns = [
    re_path(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
            GalleryDateDetailView.as_view(month_format='%m'),
            name='gallery-detail'),
    re_path(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
            GalleryDayArchiveView.as_view(month_format='%m'),
            name='gallery-archive-day'),
    re_path(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
            GalleryMonthArchiveView.as_view(month_format='%m'),
            name='gallery-archive-month'),
    re_path(r'^gallery/(?P<year>\d{4})/$',
            GalleryYearArchiveView.as_view(),
            name='pl-gallery-archive-year'),
    path('gallery/',
         GalleryArchiveIndexView.as_view(),
         name='pl-gallery-archive'),
    path('',
         RedirectView.as_view(
             url=reverse_lazy('photologue:pl-gallery-archive'), permanent=True),
         name='pl-photologue-root'),
    re_path(r'^gallery/(?P<slug>[\-\d\w]+)/$',
            GalleryDetailView.as_view(), name='pl-gallery'),
    path('gallerylist/',
         GalleryListView.as_view(),
         name='gallery-list'),

    re_path(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
            PhotoDateDetailView.as_view(month_format='%m'),
            name='photo-detail'),
    re_path(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
            PhotoDayArchiveView.as_view(month_format='%m'),
            name='photo-archive-day'),
    re_path(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
            PhotoMonthArchiveView.as_view(month_format='%m'),
            name='photo-archive-month'),
    re_path(r'^photo/(?P<year>\d{4})/$',
            PhotoYearArchiveView.as_view(),
            name='pl-photo-archive-year'),
    path('photo/',
         PhotoArchiveIndexView.as_view(),
         name='pl-photo-archive'),

    re_path(r'^photo/(?P<slug>[\-\d\w]+)/$',
            PhotoDetailView.as_view(),
            name='pl-photo'),
    path('photolist/',
         PhotoListView.as_view(),
         name='photo-list'),
]
