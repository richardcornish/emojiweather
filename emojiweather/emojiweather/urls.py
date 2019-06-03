from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import FaviconView, HomeView, RobotsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('search/', include('search.urls')),
    path('text/', include('sms.urls')),
    path('call/', include('voice.urls')),
    path('commands/', include('commands.urls')),
    path('favicon.ico', FaviconView.as_view(), name='favicon'),
    path('robots.txt', RobotsView.as_view(), name='robots'),
    path('sitemap.xml', include('sitemaps.urls')),
    path('', HomeView.as_view(), name='home'),
]


if getattr(settings, 'DEBUG', False):
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
