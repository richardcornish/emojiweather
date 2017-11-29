from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from .sitemaps import sitemaps


urlpatterns = [
    url(r'^$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
