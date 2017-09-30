from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import FaviconView, HomeView, SmsView, VoiceView

import debug_toolbar


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sms/$', SmsView.as_view(), name='sms'),
    url(r'^voice/$', VoiceView.as_view(), name='voice'),
    url(r'^favicon\.ico$', FaviconView.as_view(), name='favicon'),
    url(r'^$', HomeView.as_view(), name='home'),
]


# Static/media for local development
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]