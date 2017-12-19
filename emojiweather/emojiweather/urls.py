from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import debug_toolbar

from .views import FaviconView, HomeView, RobotsView


urlpatterns = [
    url(r'^about/', include('about.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('search.urls')),
    url(r'^text/', include('sms.urls')),
    url(r'^call/', include('voice.urls')),
    url(r'^favicon\.ico$', FaviconView.as_view(), name='favicon'),
    url(r'^robots\.txt$', RobotsView.as_view(), name='robots'),
    url(r'^', include('sitemaps.urls')),
    url(r'^$', HomeView.as_view(), name='home'),
]


# Static/media for local development
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
