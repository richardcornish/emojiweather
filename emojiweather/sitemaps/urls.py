from django.conf.urls import url
from django.contrib.sitemaps import views

from .sitemaps import sitemaps


urlpatterns = [
    url(r'^sitemap\.xml$', views.sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
