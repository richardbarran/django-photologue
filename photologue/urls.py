from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from models import *
from django.views.generic.list import ListView

# Number of random images from the gallery to display.
from photologue.views import PhotoListView, PhotoDetailView, GalleryListView, GalleryDetailView

SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)

# galleries
gallery_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}
urlpatterns = patterns('django.views.generic.date_based',
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'date_field': 'date_added', 'slug_field': 'title_slug', 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}, name='pl-gallery-detail'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', gallery_args, name='pl-gallery-archive-day'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', gallery_args, name='pl-gallery-archive-month'),
    url(r'^gallery/(?P<year>\d{4})/$', 'archive_year', gallery_args, name='pl-gallery-archive-year'),
    url(r'^gallery/?$', 'archive_index', gallery_args, name='pl-gallery-archive'),
)

# photographs
photo_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Photo.objects.filter(is_public=True)}
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 'object_detail', {'date_field': 'date_added', 'slug_field': 'title_slug', 'queryset': Photo.objects.filter(is_public=True)}, name='pl-photo-detail'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', photo_args, name='pl-photo-archive-day'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', photo_args, name='pl-photo-archive-month'),
    url(r'^photo/(?P<year>\d{4})/$', 'archive_year', photo_args, name='pl-photo-archive-year'),
    url(r'^photo/$', 'archive_index', photo_args, name='pl-photo-archive'),
)

urlpatterns += patterns('',

    url(r'^gallery/(?P<slug>[\-\d\w]+)/$', GalleryDetailView.as_view() , name='pl-gallery'),
    url(r'^gallery/page/(?P<page>[0-9]+)/$', GalleryListView.as_view(), name='pl-gallery-list'),

    url(r'^photo/(?P<slug>[\-\d\w]+)/$', PhotoDetailView.as_view() , name='pl-photo'),
    url(r'^photo/page/(?P<page>[0-9]+)/$', PhotoListView.as_view(), name='pl-photo-list'),

)


