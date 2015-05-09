from django.conf.urls import *
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from .views import PhotoListView, PhotoDetailView, GalleryListView, \
    GalleryDetailView, PhotoArchiveIndexView, PhotoDateDetailView, PhotoDayArchiveView, \
    PhotoYearArchiveView, PhotoMonthArchiveView, GalleryArchiveIndexView, GalleryYearArchiveView, \
    GalleryDateDetailView, GalleryDayArchiveView, GalleryMonthArchiveView, GalleryDateDetailOldView, \
    GalleryDayArchiveOldView, GalleryMonthArchiveOldView, PhotoDateDetailOldView, \
    PhotoDayArchiveOldView, PhotoMonthArchiveOldView

"""NOTE: the url names are changing. In the long term, I want to remove the 'pl-'
prefix on all urls, and instead rely on an application namespace 'photologue'.

At the same time, I want to change some URL patterns, e.g. for pagination. Changing the urls
twice within a few releases, could be confusing, so instead I am updating URLs bit by bit.

The new style will coexist with the existing 'pl-' prefix for a couple of releases.

"""


urlpatterns = patterns('',

                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           GalleryDateDetailView.as_view(month_format='%m'),
                           name='gallery-detail'),
                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
                           GalleryDayArchiveView.as_view(month_format='%m'),
                           name='gallery-archive-day'),
                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
                           GalleryMonthArchiveView.as_view(month_format='%m'),
                           name='gallery-archive-month'),
                       url(r'^gallery/(?P<year>\d{4})/$',
                           GalleryYearArchiveView.as_view(),
                           name='pl-gallery-archive-year'),
                       url(r'^gallery/$',
                           GalleryArchiveIndexView.as_view(),
                           name='pl-gallery-archive'),
                       url(r'^$',
                           RedirectView.as_view(
                               url=reverse_lazy('photologue:pl-gallery-archive'), permanent=True),
                           name='pl-photologue-root'),
                       url(r'^gallery/(?P<slug>[\-\d\w]+)/$',
                           GalleryDetailView.as_view(), name='pl-gallery'),
                       url(r'^gallerylist/$',
                           GalleryListView.as_view(),
                           name='gallery-list'),

                       url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           PhotoDateDetailView.as_view(month_format='%m'),
                           name='photo-detail'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
                           PhotoDayArchiveView.as_view(month_format='%m'),
                           name='photo-archive-day'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
                           PhotoMonthArchiveView.as_view(month_format='%m'),
                           name='photo-archive-month'),
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
                           name='photo-list'),

                       # Deprecated URLs.
                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           GalleryDateDetailOldView.as_view(),
                           name='pl-gallery-detail'),
                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
                           GalleryDayArchiveOldView.as_view(),
                           name='pl-gallery-archive-day'),
                       url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
                           GalleryMonthArchiveOldView.as_view(),
                           name='pl-gallery-archive-month'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           PhotoDateDetailOldView.as_view(),
                           name='pl-photo-detail'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
                           PhotoDayArchiveOldView.as_view(),
                           name='pl-photo-archive-day'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
                           PhotoMonthArchiveOldView.as_view(),
                           name='pl-photo-archive-month')
                       )
