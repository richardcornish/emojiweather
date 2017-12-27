from django import forms

from emojiweather.mixins import WeatherFormMixin


class VoiceWeatherForm(WeatherFormMixin, forms.Form):
    Digits = forms.CharField(required=False)
    SpeechResult = forms.CharField(required=False)
