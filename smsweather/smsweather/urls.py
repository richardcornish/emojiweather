from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import SmsView, FaviconView, HomeView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sms/$', SmsView.as_view(), name='sms'),
    url(r'^favicon\.ico$', FaviconView.as_view(), name='favicon'),
    url(r'^$', HomeView.as_view(), name='home'),
]


# Static/media for local development
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
