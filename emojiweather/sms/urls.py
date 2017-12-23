from django.urls import path

from .views import SmsView


urlpatterns = [
    path('', SmsView.as_view(), name='sms'),
]
