from django.urls import path

from .views import WhatsAppView


urlpatterns = [
    path('', WhatsAppView.as_view(), name='whatsapp'),
]
