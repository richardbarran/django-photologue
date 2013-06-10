from django.conf.urls import *

from photologue.sitemaps import GallerySitemap, PhotoSitemap

# Note: this urls definition file is used only for sitemap tests at the moment.
# Maybe it should be extended at a later date?

urlpatterns = patterns('',
    (r'^photologue/', include('photologue.urls')),
)

sitemaps = {'photologue_galleries': GallerySitemap,
            'photologue_photos': PhotoSitemap,
}

urlpatterns += patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': \
                                                                      sitemaps})
)
