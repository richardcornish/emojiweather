from django.urls import path

from .views import SearchView


urlpatterns = [
    path(r'', SearchView.as_view(), name='search'),
]
