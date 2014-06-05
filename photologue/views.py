from django.conf import settings
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Photo, Gallery
from django.core.urlresolvers import reverse

#import logging
#logger = logging.getLogger(__name__)

# Number of galleries to display per page.
GALLERY_PAGINATE_BY = getattr(settings, 'PHOTOLOGUE_GALLERY_PAGINATE_BY', 20)

if GALLERY_PAGINATE_BY != 20:
    import warnings
    warnings.warn(
        DeprecationWarning('PHOTOLOGUE_GALLERY_PAGINATE_BY setting will be removed in Photologue 3.0'))

# Number of photos to display per page.
PHOTO_PAGINATE_BY = getattr(settings, 'PHOTOLOGUE_PHOTO_PAGINATE_BY', 20)

if PHOTO_PAGINATE_BY != 20:
    import warnings
    warnings.warn(
        DeprecationWarning('PHOTOLOGUE_PHOTO_PAGINATE_BY setting will be removed in Photologue 3.0'))

# Gallery views.


class GalleryListView(ListView):
    queryset = Gallery.objects.on_site().is_public()
    paginate_by = GALLERY_PAGINATE_BY


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
    #queryset = Gallery.objects.on_site().is_public()[:1]


class GalleryDayArchiveView(GalleryDateView, DayArchiveView):
    pass


class GalleryMonthArchiveView(GalleryDateView, MonthArchiveView):
    pass


class GalleryYearArchiveView(GalleryDateView, YearArchiveView):
    pass

# Photo views.


class PhotoListView(ListView):
    queryset = Photo.objects.on_site().is_public()
    paginate_by = PHOTO_PAGINATE_BY

class PhotoDetailView(DetailView):
    queryset = Photo.objects.on_site().is_public()


#-----------------------------------------
# CF20140602 
# adding editable caption via UpdateView and mixin.
# PhotoUpdateView replaces PhotoDetailView in photologue/urls.py

from django.contrib import messages

class CaptionActionMixin(object):
    """Caption mixin for editing as photo caption.
    """
    fields = ('caption',)

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        """Edited caption data is saved when valid.
        """
        messages.info(self.request, self.success_msg)
        self.object = form.save()
        return super(CaptionActionMixin, self).form_valid(form)


class PhotoUpdateView(CaptionActionMixin, UpdateView):
    """Make caption updateable.
    """
    model = Photo
    fields = ('caption',)
    queryset = Photo.objects.on_site().is_public()

    def get_context_data(self, **kwargs):
        """Size the caption box to the length of the caption [initially just 
        using 50-character rows as a default].
        """
        context = super(PhotoUpdateView, self).get_context_data(**kwargs)
        columns = 50
        length = len(self.object.caption)
        from math import ceil
        context["caption_rows"] = ceil(length/columns)
        return context

#-----------------------------------------

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
    pass
