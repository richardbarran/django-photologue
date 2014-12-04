"""
The `Sitemaps protocol <http://en.wikipedia.org/wiki/Sitemaps>`_ allows a webmaster
to inform search engines about URLs on a website that are available for crawling.
Django comes with a high-level framework that makes generating sitemap XML files easy.

Install the sitemap application as per the `instructions in the django documentation
<https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/>`_, then edit your
project's ``urls.py`` and add a reference to Photologue's Sitemap classes in order to
included all the publicly-viewable Photologue pages:

.. code-block:: python

    ...
    from photologue.sitemaps import GallerySitemap, PhotoSitemap

    sitemaps = {...
                'photologue_galleries': GallerySitemap,
                'photologue_photos': PhotoSitemap,
                ...
                }
    etc...

There are 2 sitemap classes, as in some cases you may want to have gallery pages,
but no photo detail page (e.g. if all photos are displayed via a javascript
lightbox).

"""
from django.contrib.sitemaps import Sitemap
from .models import Gallery, Photo

# Note: Gallery and Photo are split, because there are use cases for having galleries
# in the sitemap, but not photos (e.g. if the photos are displayed with a lightbox).


class GallerySitemap(Sitemap):

    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Gallery.objects.on_site().is_public()

    def lastmod(self, obj):
        return obj.date_added


class PhotoSitemap(Sitemap):

    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Photo.objects.on_site().is_public()

    def lastmod(self, obj):
        return obj.date_added
