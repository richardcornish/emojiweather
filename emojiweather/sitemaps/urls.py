from django.contrib.sitemaps import views
from django.urls import path

from .sitemaps import sitemaps


urlpatterns = [
    path('', views.sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
