from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from ..sitemaps import GallerySitemap, PhotoSitemap

urlpatterns = [
    path('ptests/', include('photologue.urls', namespace='photologue')),
]

sitemaps = {'photologue_galleries': GallerySitemap,
            'photologue_photos': PhotoSitemap,
            }

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]
