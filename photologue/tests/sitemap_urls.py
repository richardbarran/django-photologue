from django.conf.urls.defaults import *

from photologue.sitemaps import PhotologueSitemap

# Note: this urls definition file is used only for sitemap tests at the moment.
# Maybe it should be extended at a later date?

urlpatterns = patterns('',
    (r'^photologue/', include('photologue.urls')),
)

sitemaps = {'photologue': PhotologueSitemap
}

urlpatterns += patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': \
                                                                      sitemaps})
)
