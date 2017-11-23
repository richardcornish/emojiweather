from django.conf.urls import url

from .views import SmsView


urlpatterns = [
    url(r'^$', SmsView.as_view(), name='sms'),
]
