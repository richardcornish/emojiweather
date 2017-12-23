from django.urls import path

from .views import VoiceView


urlpatterns = [
    path('', VoiceView.as_view(), name='voice'),
]
