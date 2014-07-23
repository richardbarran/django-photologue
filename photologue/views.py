import warnings

from django.conf import settings
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Photo, Gallery

# Number of galleries to display per page.
GALLERY_PAGINATE_BY = getattr(settings, 'PHOTOLOGUE_GALLERY_PAGINATE_BY', 20)

if GALLERY_PAGINATE_BY != 20:
    warnings.warn(
        DeprecationWarning('PHOTOLOGUE_GALLERY_PAGINATE_BY setting will be removed in Photologue 3.1'))

# Number of photos to display per page.
PHOTO_PAGINATE_BY = getattr(settings, 'PHOTOLOGUE_PHOTO_PAGINATE_BY', 20)

if PHOTO_PAGINATE_BY != 20:
    warnings.warn(
        DeprecationWarning('PHOTOLOGUE_PHOTO_PAGINATE_BY setting will be removed in Photologue 3.1'))

# Gallery views.


class GalleryListView(ListView):
    queryset = Gallery.objects.on_site().is_public()
    paginate_by = GALLERY_PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        if self.kwargs.get('deprecated_pagination', False):
            warnings.warn(
                DeprecationWarning('Page numbers should now be passed via a page query-string parameter.'
                                   ' The old style "/page/n/"" will be removed in Photologue 3.2'))
        return context


class GalleryDetailView(DetailView):
    queryset = Gallery.objects.on_site().is_public()


class GalleryDateView(object):
    queryset = Gallery.objects.on_site().is_public()
    date_field = 'date_added'
    allow_empty = True


class GalleryDateDetailView(GalleryDateView, DateDetailView):
    pass


class GalleryArchiveIndexView(GalleryDateView, ArchiveIndexView):
    pass


class GalleryDayArchiveView(GalleryDateView, DayArchiveView):
    pass


class GalleryMonthArchiveView(GalleryDateView, MonthArchiveView):
    pass


class GalleryYearArchiveView(GalleryDateView, YearArchiveView):
    make_object_list = True

# Photo views.


class PhotoListView(ListView):
    queryset = Photo.objects.on_site().is_public()
    paginate_by = PHOTO_PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        if self.kwargs.get('deprecated_pagination', False):
            warnings.warn(
                DeprecationWarning('Page numbers should now be passed via a page query-string parameter.'
                                   ' The old style "/page/n/"" will be removed in Photologue 3.2'))
        return context


class PhotoDetailView(DetailView):
    queryset = Photo.objects.on_site().is_public()


class PhotoDateView(object):
    queryset = Photo.objects.on_site().is_public()
    date_field = 'date_added'
    allow_empty = True


class PhotoDateDetailView(PhotoDateView, DateDetailView):
    pass


class PhotoArchiveIndexView(PhotoDateView, ArchiveIndexView):
    pass


class PhotoDayArchiveView(PhotoDateView, DayArchiveView):
    pass


class PhotoMonthArchiveView(PhotoDateView, MonthArchiveView):
    pass


class PhotoYearArchiveView(PhotoDateView, YearArchiveView):
    make_object_list = True
