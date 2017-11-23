from django import forms

from emojiweather.mixins import WeatherMixin


class VoiceWeatherForm(WeatherMixin, forms.Form):
    Digits = forms.CharField(required=False)
    SpeechResult = forms.CharField(required=False)
    FromCity = forms.CharField(required=False)
    FromState = forms.CharField(required=False)
    FromZip = forms.CharField(required=False)
    FromCountry = forms.CharField(required=False)
