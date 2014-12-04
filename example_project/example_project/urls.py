from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^photologue/', include('photologue.urls', namespace='photologue')),
                       url(r'^$', TemplateView.as_view(
                           template_name="homepage.html"), name='homepage'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
