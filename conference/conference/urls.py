from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import ConferenceView, WeatherView, HomeView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^conference/$', ConferenceView.as_view(), name='conference'),
    url(r'^weather/$', WeatherView.as_view(), name='weather'),
    url(r'^$', HomeView.as_view(), name='home'),
]

# Static/media for local development
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns()
