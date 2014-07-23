from django.conf.urls import *
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from .views import PhotoListView, PhotoDetailView, GalleryListView, \
    GalleryDetailView, PhotoArchiveIndexView, PhotoDateDetailView, PhotoDayArchiveView, \
    PhotoYearArchiveView, PhotoMonthArchiveView, GalleryArchiveIndexView, GalleryYearArchiveView, \
    GalleryDateDetailView, GalleryDayArchiveView, GalleryMonthArchiveView

"""NOTE: the url names are changing. In the long term, I want the prefix on all url names to be 'photologue-'
rather than 'pl-'.
This is simply to follow the Zen of Python - "Explicit is better than implicit".

At the same time, I want to change some URL patterns, e.g. for pagination.

So I've started changing the pagination to a new style prefix 'photologue-', and this will
coexist with the existing 'pl-' for some time.

"""


urlpatterns = patterns('',

                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           GalleryDateDetailView.as_view(),
                           name='pl-gallery-detail'),
                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
                           GalleryDayArchiveView.as_view(),
                           name='pl-gallery-archive-day'),
                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
                           GalleryMonthArchiveView.as_view(),
                           name='pl-gallery-archive-month'),
                       url(r'^gallery/(?P<year>\d{4})/$',
                           GalleryYearArchiveView.as_view(),
                           name='pl-gallery-archive-year'),
                       url(r'^gallery/$',
                           GalleryArchiveIndexView.as_view(),
                           name='pl-gallery-archive'),
                       url(r'^$',
                           RedirectView.as_view(url=reverse_lazy('pl-gallery-archive')),
                           name='pl-photologue-root'),
                       url(r'^gallery/(?P<slug>[\-\d\w]+)/$',
                           GalleryDetailView.as_view(), name='pl-gallery'),
                       url(r'^gallerylist/$',
                           GalleryListView.as_view(),
                           name='photologue-gallery-list'),

                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           PhotoDateDetailView.as_view(),
                           name='pl-photo-detail'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
                           PhotoDayArchiveView.as_view(),
                           name='pl-photo-archive-day'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
                           PhotoMonthArchiveView.as_view(),
                           name='pl-photo-archive-month'),
                       url(r'^photo/(?P<year>\d{4})/$',
                           PhotoYearArchiveView.as_view(),
                           name='pl-photo-archive-year'),
                       url(r'^photo/$',
                           PhotoArchiveIndexView.as_view(),
                           name='pl-photo-archive'),

                       url(r'^photo/(?P<slug>[\-\d\w]+)/$',
                           PhotoDetailView.as_view(),
                           name='pl-photo'),
                       url(r'^photolist/$',
                           PhotoListView.as_view(),
                           name='photologue-photo-list'),

                       # Deprecated URLs.
                       url(r'^gallery/page/(?P<page>[0-9]+)/$',
                           GalleryListView.as_view(),
                           {'deprecated_pagination': True},
                           name='pl-gallery-list'),
                       url(r'^photo/page/(?P<page>[0-9]+)/$',
                           PhotoListView.as_view(),
                           {'deprecated_pagination': True},
                           name='pl-photo-list'),


                       )
