from django.conf.urls import url

from .views import VoiceView


urlpatterns = [
    url(r'^$', VoiceView.as_view(), name='voice'),
]
