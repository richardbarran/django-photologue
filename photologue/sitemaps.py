"""
Photologue can be used in your site's sitemap.xml to generate a list of all the 
Gallery and Photo pages.

To use, add the following to the sitemap definition section of your project's
urls.py::

    ...
    from photologue.sitemaps import GallerySitemap, PhotoSitemap
    
    sitemaps = {...
                'photologue_galleries': GallerySitemap,
                'photologue_photos': PhotoSitemap,
                ...
                }
    etc...

.. note::
    
    There is also a PhotologueSitemap class which combines the above 2 classes,
    but it will be removed in Photologue 3.0.
"""
import warnings

from django.contrib.sitemaps import Sitemap
from .models import Gallery, Photo

# Note: Gallery and Photo are split, because there are use cases for having galleries
# in the sitemap, but not photos (e.g. if the photos are displayed with a lightbox).

class GallerySitemap(Sitemap):
    priority = 0.5

    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Gallery.objects.filter(is_public=True)

    def lastmod(self, obj):
            return obj.date_added

class PhotoSitemap(Sitemap):
    priority = 0.5

    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Photo.objects.filter(is_public=True)

    def lastmod(self, obj):
            return obj.date_added

class PhotologueSitemap(Sitemap):
    priority = 0.5

    def items(self):
        warnings.warn(DeprecationWarning('PhotologueSitemap will be replaced in '
        'Photologue 3.0 by GallerySitemap and PhotoSitemap.'))
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return list(Gallery.objects.filter(is_public=True)) \
                                    + list(Photo.objects.filter(is_public=True))

    def lastmod(self, obj):
            return obj.date_added

