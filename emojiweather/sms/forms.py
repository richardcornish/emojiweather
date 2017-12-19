from django import forms

from emojiweather.mixins import WeatherFormMixin


class SmsWeatherForm(WeatherFormMixin, forms.Form):
    Body = forms.CharField()
