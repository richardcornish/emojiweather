from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import debug_toolbar

from sms.views import SmsView
from voice.views import VoiceView
from .views import FaviconView, HomeView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sms/$', SmsView.as_view(), name='sms'),
    url(r'^voice/$', VoiceView.as_view(), name='voice'),
    url(r'^favicon\.ico$', FaviconView.as_view(), name='favicon'),
    url(r'^$', HomeView.as_view(), name='home'),
]


# Static/media for local development
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
