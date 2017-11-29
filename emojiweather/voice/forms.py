from django import forms

from emojiweather.mixins import WeatherFormMixin


class VoiceWeatherForm(WeatherFormMixin, forms.Form):
    Digits = forms.CharField(required=False)
    SpeechResult = forms.CharField(required=False)
    FromCity = forms.CharField(required=False)
    FromState = forms.CharField(required=False)
    FromZip = forms.CharField(required=False)
    FromCountry = forms.CharField(required=False)
