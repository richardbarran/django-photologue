from django.conf.urls import *
from ..sitemaps import GallerySitemap, PhotoSitemap

urlpatterns = patterns('',
                       (r'^ptests/', include('photologue.urls', namespace='photologue')),
                       )

sitemaps = {'photologue_galleries': GallerySitemap,
            'photologue_photos': PhotoSitemap,
            }

urlpatterns += patterns('',
                        (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':
                                                                                     sitemaps})
                        )
