from django.urls import path

from .views import AboutView


urlpatterns = [
    path(r'', AboutView.as_view(), name='about'),
]
